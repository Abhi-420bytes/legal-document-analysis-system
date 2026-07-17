import os
import sys
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.pipeline.document_parser import DocumentParser
from backend.pipeline.ner_pipeline import LegalNER
from backend.pipeline.classifier import CaseTypeClassifier
from backend.pipeline.clause_extractor import ClauseExtractor
from backend.pipeline.case_retriever import CaseRetriever
from backend.data.legal_sections_db import get_sections_for_case_type

app = FastAPI(title="Legal Document Analysis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline components once at startup
parser = DocumentParser()
ner = LegalNER()
classifier = CaseTypeClassifier()
clause_extractor = ClauseExtractor()
retriever = CaseRetriever(db_path="./case_database")


class TextAnalysisRequest(BaseModel):
    text: str


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Legal Analysis API is running"}


@app.post("/analyze/file")
async def analyze_file(file: UploadFile = File(...)):
    allowed = {".pdf", ".docx", ".txt"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        text = parser.parse(tmp_path)
        return _run_pipeline(text)
    finally:
        os.unlink(tmp_path)


@app.post("/analyze/text")
def analyze_text(req: TextAnalysisRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return _run_pipeline(req.text)


@app.get("/sections/{case_type}")
def get_sections(case_type: str):
    sections = get_sections_for_case_type(case_type)
    if not sections:
        raise HTTPException(status_code=404, detail=f"No sections found for case type: {case_type}")
    return {"case_type": case_type, "sections": sections}


def _run_pipeline(text: str) -> dict:
    entities = ner.extract_entities(text)
    case_type_result = classifier.predict(text)
    clauses = clause_extractor.extract_clauses(text)
    similar_cases = retriever.find_similar(text[:500], n=5)
    applicable_sections = get_sections_for_case_type(case_type_result["case_type"])

    return {
        "status": "success",
        "text_preview": text[:500],
        "entities": entities,
        "case_type": case_type_result,
        "clauses": clauses,
        "applicable_sections": applicable_sections[:10],
        "similar_cases": similar_cases,
    }
