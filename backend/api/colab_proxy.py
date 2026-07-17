"""
Lightweight local proxy — forwards model calls to the Colab API.

Accuracy results (40-case test set):
  Model 1  BART large-mnli (zero-shot)      87.5%  ← BEST, used as default
  Model 2  DeBERTa-v3-large (zero-shot)     72.5%
  Ensemble M1×0.9 + M2×0.1                 87.5%
  Fine-tuned (LEDGAR hybrid)               32.5%  ← LEDGAR is contract-only, poor for Indian courts

Usage:
  1. Open notebooks/legal_analysis_colab.ipynb in Colab (T4 GPU)
  2. Run all cells — Colab prints a public ngrok URL
  3. Set COLAB_API_URL=<that_url> in .env
  4. Run: uvicorn backend.api.colab_proxy:app --reload --port 8000
"""

import os
import re
import sys
import tempfile

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

COLAB_URL = os.getenv("COLAB_API_URL", "").rstrip("/")

# Model 1 (BART) is the best-performing model — 87.5% on 40-case test set
DEFAULT_MODEL_ENDPOINT = "/analyze/model1"

app = FastAPI(title="Legal Analysis API", version="3.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from backend.pipeline.document_parser import DocumentParser
from backend.pipeline.ner_pipeline import LegalNER
from backend.pipeline.clause_extractor import ClauseExtractor
from backend.pipeline.case_retriever import CaseRetriever
from backend.pipeline.classifier import CaseTypeClassifier
from backend.data.legal_sections_db import get_sections_for_case_type

parser         = DocumentParser()
ner            = LegalNER()
clause_extractor = ClauseExtractor()
retriever      = CaseRetriever(db_path=os.path.join(os.path.dirname(__file__), "..", "..", "case_database"))
classifier     = CaseTypeClassifier()   # BART large-mnli — downloads once, then cached


class TextRequest(BaseModel):
    text: str


def _colab_ok() -> bool:
    return bool(COLAB_URL)


NGROK_HEADERS = {
    "ngrok-skip-browser-warning": "true",
    "User-Agent": "LegalAnalysisProxy/1.0",
}

async def _call_colab(endpoint: str, text: str) -> dict:
    async with httpx.AsyncClient(timeout=120) as client:
        try:
            resp = await client.post(
                f"{COLAB_URL}{endpoint}",
                json={"text": text},
                headers=NGROK_HEADERS,
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.TimeoutException:
            return {"error": "Colab timed out — models may still be loading, retry in 30s"}
        except Exception as e:
            return {"error": str(e)}


# ── Summarisation ─────────────────────────────────────────────────────────────

_LEGAL_TERMS = {
    "accused","plaintiff","defendant","petitioner","respondent","appellant",
    "court","judge","judgment","decree","order","injunction","writ",
    "section","ipc","cpc","crpc","act","offence","crime","criminal",
    "contract","breach","damages","compensation","relief","remedy",
    "filed","appeal","petition","suit","complaint","fir","charge",
    "convicted","acquitted","bail","imprisonment","sentence","fine",
    "murder","theft","fraud","negligence","liability","violation",
    "rs.","rupees","lakh","crore","payment","property","land",
    "marriage","divorce","custody","maintenance","alimony",
    "patent","trademark","copyright","infringement","labour","workman",
}

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

def _summarize_local(text: str, n: int = 5) -> str:
    sentences = [s.strip() for s in _SENT_SPLIT.split(text) if len(s.strip()) > 40]
    if not sentences:
        return text[:500]
    if len(sentences) <= n:
        return " ".join(sentences)

    scored = []
    for i, sent in enumerate(sentences):
        words   = re.findall(r"\b\w+\b", sent.lower())
        legal   = sum(1 for w in words if w in _LEGAL_TERMS)
        pos     = 1.5 if i < 3 else (1.2 if i < 6 else 1.0)
        length  = min(len(words), 35) / 35
        scored.append((legal * 2 + pos + length, i, sent))

    top = sorted(scored, key=lambda x: -x[0])[:n]
    top.sort(key=lambda x: x[1])
    return " ".join(s for _, _, s in top)


def _summarize_claude(text: str) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=350,
            messages=[{
                "role": "user",
                "content": (
                    "Summarize this Indian legal document in 4–5 sentences. "
                    "Cover: parties involved, legal issue, key facts, relief sought, "
                    "and relevant law sections mentioned.\n\n" + text[:3500]
                ),
            }],
        )
        return msg.content[0].text
    except Exception as e:
        return _summarize_local(text)


def _summarize(text: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if api_key and not api_key.startswith("sk-ant-xxx"):
        return _summarize_claude(text)
    return _summarize_local(text)


def _local_fallback(text: str) -> dict:
    entities   = ner.extract_entities(text)
    clauses    = clause_extractor.extract_clauses(text)
    cls_result = classifier.predict(text)
    ct         = cls_result.get("case_type", "civil")
    return {
        "status":               "local",
        "summary":              _summarize(text),
        "entities":             entities,
        "classification":       {**cls_result, "model": "bart-large-mnli (local)"},
        "case_type":            cls_result,
        "clauses":              clauses,
        "similar_cases":        retriever.find_similar(text[:500], n=3),
        "applicable_sections":  get_sections_for_case_type(ct)[:10],
    }


async def _analyze(text: str, endpoint: str) -> dict:
    text = text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is empty")

    if not _colab_ok():
        return _local_fallback(text)

    result = await _call_colab(endpoint, text)

    if "error" in result:
        # Colab unreachable — run fully local with BART
        fallback = _local_fallback(text)
        fallback["colab_error"] = result["error"]
        return fallback

    # Enrich with summary, similar cases, applicable legal sections (all local)
    cls = result.get("classification", result.get("case_type", {}))
    ct  = cls.get("case_type", "civil") if isinstance(cls, dict) else "civil"
    result["applicable_sections"] = get_sections_for_case_type(ct)[:10]
    result["summary"]              = _summarize(text)
    result["similar_cases"]        = retriever.find_similar(text[:500], n=3)
    result["endpoint_used"]        = endpoint
    return result


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/")
def health():
    return {
        "status":          "ok",
        "colab_connected": _colab_ok(),
        "colab_url":       COLAB_URL or "not set — add COLAB_API_URL to .env",
        "default_model":   "model1 (BART large-mnli, 87.5% accuracy)",
        "accuracy_results": {
            "model1_BART":           "87.5%  ← zero-shot baseline",
            "inlegal_bert":          "target 92–95%  ← InLegalBERT Indian fine-tuned (Cell 9E)",
            "model2_DeBERTa_v3":     "72.5%",
            "ensemble_M1xM2":        "87.5%",
            "finetuned_LEDGAR":      "32.5%  (wrong domain — LEDGAR=SEC contracts)",
        },
        "endpoints": [
            "POST /analyze          ← default (Model 1, best zero-shot)",
            "POST /analyze/file     ← upload PDF / DOCX / TXT",
            "POST /analyze/model1   ← BART large-mnli (87.5%)",
            "POST /analyze/model2   ← DeBERTa-v3-large (72.5%)",
            "POST /analyze/inlegal  ← InLegalBERT Indian fine-tuned (run Cell 9E first)",
            "POST /analyze/ensemble ← weighted M1+M2",
            "POST /compare          ← side-by-side comparison",
            "POST /embed/model1     ← MiniLM embeddings",
            "POST /embed/model2     ← Legal-BERT embeddings",
            "GET  /sections/{case_type}",
        ],
    }


# ── Primary endpoint — Model 1 by default ────────────────────────────────────

@app.post("/analyze")
async def analyze(req: TextRequest):
    """Default endpoint — uses Model 1 (BART, 87.5% accuracy)."""
    return await _analyze(req.text, DEFAULT_MODEL_ENDPOINT)


# ── File upload ───────────────────────────────────────────────────────────────

@app.post("/analyze/file")
async def analyze_file(file: UploadFile = File(...)):
    """Upload PDF, DOCX, or TXT — runs Model 1 (best accuracy)."""
    allowed = {".pdf", ".docx", ".txt"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        text = parser.parse(tmp_path)
    finally:
        os.unlink(tmp_path)

    return await _analyze(text, DEFAULT_MODEL_ENDPOINT)


# ── Individual model endpoints ────────────────────────────────────────────────

@app.post("/analyze/model1")
async def analyze_model1(req: TextRequest):
    """BART large-mnli zero-shot — 87.5% accuracy on legal case test set."""
    return await _analyze(req.text, "/analyze/model1")


@app.post("/analyze/model2")
async def analyze_model2(req: TextRequest):
    """DeBERTa-v3-large zero-shot — 72.5% accuracy."""
    return await _analyze(req.text, "/analyze/model2")


@app.post("/analyze/inlegal")
async def analyze_inlegal(req: TextRequest):
    """InLegalBERT fine-tuned on Indian legal data — run Cell 9E in Colab first."""
    return await _analyze(req.text, "/analyze/inlegal")


@app.post("/analyze/ensemble")
async def analyze_ensemble(req: TextRequest):
    """Weighted ensemble M1×0.9 + M2×0.1 — matches Model 1 accuracy."""
    return await _analyze(req.text, "/analyze/ensemble")


@app.post("/compare")
async def compare(req: TextRequest):
    """Side-by-side comparison of Model 1 vs Model 2."""
    if not _colab_ok():
        raise HTTPException(status_code=503, detail="Colab not connected")
    result = await _call_colab("/compare", req.text)
    if "error" in result:
        raise HTTPException(status_code=502, detail=result["error"])
    return result


@app.post("/embed/model1")
async def embed_model1(req: TextRequest):
    if not _colab_ok():
        raise HTTPException(status_code=503, detail="Colab not connected")
    return await _call_colab("/embed/model1", req.text)


@app.post("/embed/model2")
async def embed_model2(req: TextRequest):
    if not _colab_ok():
        raise HTTPException(status_code=503, detail="Colab not connected")
    return await _call_colab("/embed/model2", req.text)


# ── Legal sections (local, no Colab needed) ───────────────────────────────────

@app.get("/sections/{case_type}")
def get_sections(case_type: str):
    sections = get_sections_for_case_type(case_type)
    if not sections:
        raise HTTPException(status_code=404, detail=f"No sections for: {case_type}")
    return {"case_type": case_type, "sections": sections}
