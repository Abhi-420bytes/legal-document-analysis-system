# Multi-Domain Legal Document Context Analysis and Clause Identification System

A full-stack NLP system that automatically analyzes Indian legal documents — classifying case type, extracting named entities, identifying clauses, summarizing content, and retrieving similar precedent cases using Retrieval-Augmented Generation (RAG).

---

## Features

- **Zero-Shot Classification** — Classifies legal documents into 8 categories using BART-large-mnli (87.5% accuracy) with no labeled training data
- **Named Entity Recognition** — Extracts parties, dates, monetary amounts, legal sections (e.g., "Section 302 IPC"), and case citations
- **Clause Identification** — Detects legal clause types: penalty, indemnity, confidentiality, termination, force majeure, etc.
- **Summarization** — Claude Haiku API (abstractive) with extractive fallback based on legal keyword scoring
- **RAG Precedent Retrieval** — BM25 + ChromaDB vector search over 80 curated Indian court cases; improves Match@1 from 88.7% to 100%
- **Applicable Sections Lookup** — Returns relevant IPC/CrPC/CPC/other statute sections by case type
- **File Upload** — Accepts PDF, DOCX, and plain-text documents
- **Web Interface** — React/Next.js frontend with results panel

---

## Case Categories

| # | Category | Example Cases |
|---|----------|---------------|
| 1 | Criminal | IPC 302 murder, NDPS drug trafficking, cyber fraud |
| 2 | Civil | Negligence, loan recovery, motor accident |
| 3 | Contract Dispute | Breach, arbitration, force majeure |
| 4 | Family Law | Divorce, custody, maintenance, dowry |
| 5 | Property | Title dispute, eviction, RERA, partition |
| 6 | Constitutional | PIL, habeas corpus, fundamental rights |
| 7 | Intellectual Property | Patent, trademark, copyright, software |
| 8 | Labour | Retrenchment, wages, gig workers, EPFO |

---

## Architecture

```
Input (PDF / DOCX / TXT)
        │
        ▼
  Document Parser
        │
        ▼
  Text Preprocessing
        │
   ┌────┴─────────────────────────────────────┐
   ▼          ▼              ▼                ▼
  NER      Clause        Classifier       Summarizer
(spaCy)   Extractor   (BART-large-mnli)  (Claude/Local)
   └────┬─────────────────────────────────────┘
        │
        ▼
  RAG Retriever (BM25 / ChromaDB)
        │
        ▼
  Legal Sections Lookup
        │
        ▼
  JSON Response → React/Next.js Frontend
```

**GPU inference** (classification) runs on Google Colab T4 via ngrok tunnel. All other components run locally.

---

## Models

| Model | Type | Accuracy | Notes |
|-------|------|----------|-------|
| BART-large-mnli | Zero-shot NLI | **87.5%** | Default; best zero-shot |
| DeBERTa-v3-large | Zero-shot NLI | 72.5% | Model 2 |
| Ensemble (M1×0.9 + M2×0.1) | Weighted | 87.5% | No gain over BART |
| InLegalBERT | Fine-tuned Indian | 92–95%* | Run Cell 9E in Colab |
| Fine-tuned DeBERTa (LEDGAR) | Supervised | 32.5% | Wrong domain — US SEC contracts |

\* Target accuracy after fine-tuning on Indian legal examples.

---

## Project Structure

```
project/
├── backend/
│   ├── api/
│   │   ├── colab_proxy.py      # FastAPI app — proxies to Colab, local fallback
│   │   └── main.py
│   ├── pipeline/
│   │   ├── classifier.py       # BART-large-mnli zero-shot classifier
│   │   ├── ner_pipeline.py     # spaCy NER + legal regex
│   │   ├── clause_extractor.py # Keyword-based clause detection
│   │   ├── case_retriever.py   # ChromaDB + BM25 retrieval
│   │   └── document_parser.py  # PDF / DOCX / TXT parser
│   └── data/
│       └── legal_sections_db.py # IPC/CrPC/CPC sections by case type
├── frontend/
│   └── src/
│       ├── pages/              # Next.js pages
│       └── components/         # ResultsPanel, UploadForm, etc.
├── notebooks/
│   └── legal_analysis_colab1.ipynb  # Colab notebook (model inference + RAG eval)
├── case_database/              # ChromaDB vector store (80 cases)
├── datasets/
│   ├── raw/
│   └── processed/
├── report/
│   └── legal_nlp_paper.tex     # IEEE conference paper (LaTeX/Overleaf)
├── seed_cases.py               # Seeds ChromaDB with 80 Indian court cases
├── test_pipeline.py            # Pipeline unit tests
├── requirements.txt
└── .env.example
```

---

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Google Colab account (for GPU model inference)

### 1. Clone and create virtual environment

```bash
git clone <repo-url>
cd project
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Paste the ngrok URL from Colab (changes every time you restart Colab)
COLAB_API_URL="https://your-ngrok-url.ngrok-free.app"

# Optional: for Claude Haiku summarization
ANTHROPIC_API_KEY=sk-ant-...

# Optional: avoids HuggingFace rate limits
HF_TOKEN=hf_...
```

### 4. Seed the case database

```bash
python seed_cases.py
```

This populates ChromaDB with all 80 Indian court cases (10 per class).

### 5. Start the backend

```bash
uvicorn backend.api.colab_proxy:app --reload --port 8000
```

API runs at `http://localhost:8000`. Open `http://localhost:8000` in a browser to see available endpoints and accuracy results.

### 6. Install and start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:3001`.

---

## Colab Setup (GPU Inference)

1. Open `notebooks/legal_analysis_colab1.ipynb` in Google Colab
2. Set runtime to **T4 GPU**: Runtime → Change runtime type → T4 GPU
3. Run all cells in order
4. Cell 10 starts an ngrok tunnel and prints a public URL
5. Copy that URL into `.env` as `COLAB_API_URL`
6. Restart the local backend — it will now route classification through Colab

> Without Colab, the backend runs fully locally using BART-large-mnli on CPU (~12s per document instead of ~0.8s).

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check + accuracy summary |
| POST | `/analyze` | Analyze text (Model 1, best accuracy) |
| POST | `/analyze/file` | Upload PDF / DOCX / TXT |
| POST | `/analyze/model1` | BART-large-mnli (87.5%) |
| POST | `/analyze/model2` | DeBERTa-v3-large (72.5%) |
| POST | `/analyze/inlegal` | InLegalBERT (run Cell 9E first) |
| POST | `/analyze/ensemble` | Weighted M1×0.9 + M2×0.1 |
| POST | `/compare` | Side-by-side Model 1 vs Model 2 |
| GET | `/sections/{case_type}` | Applicable statute sections |

### Example request

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "The accused was charged under Section 302 IPC for the murder of the deceased..."}'
```

### Example response

```json
{
  "status": "local",
  "summary": "The accused was charged under Section 302 IPC...",
  "classification": {
    "case_type": "criminal",
    "confidence": 0.94,
    "model": "bart-large-mnli (local)"
  },
  "entities": {
    "persons": ["accused", "deceased"],
    "legal_sections": ["Section 302 IPC"]
  },
  "clauses": [],
  "similar_cases": [
    {
      "title": "State v. Ramesh Kumar",
      "court": "Delhi High Court",
      "year": 2019,
      "similarity": 0.87
    }
  ],
  "applicable_sections": ["IPC Section 302", "IPC Section 300", "CrPC Section 161"]
}
```

---

## RAG Evaluation Results

Evaluated on 80 labeled queries (10 per class, K=3):

| Metric | Without RAG | With RAG | Gain |
|--------|------------|----------|------|
| Precision@3 | 0.887 | **1.000** | +11.3% |
| MRR | 0.887 | **1.000** | +11.3% |
| NDCG@3 | 0.887 | **0.990** | +10.2% |
| Match@1 | 0.887 | **1.000** | +11.3% |

RAG eliminates all misclassifications in constitutional and labour domains where keyword overlap causes baseline confusion.

---

## Running the RAG Evaluation in Colab

Open `notebooks/legal_analysis_colab1.ipynb` and run:

- **Cell 9G** — Pure Python BM25 RAG evaluation (all 80 cases, 80 queries, all metrics)
- **Cell 9H** — Confusion matrices + comparative analysis (with vs. without RAG)

Both cells use only Python standard library (`re`, `math`, `collections`) — no dependency issues.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI (Python) |
| Zero-Shot Classifier | BART-large-mnli (HuggingFace) |
| Secondary Classifier | DeBERTa-v3-large |
| Indian Legal Model | InLegalBERT (law-ai/InLegalBert) |
| NER | spaCy en_core_web_sm |
| Vector Store | ChromaDB |
| Embeddings | all-MiniLM-L6-v2 (Sentence-BERT) |
| Summarization | Claude Haiku API / Extractive fallback |
| Document Parsing | pdfplumber, python-docx |
| Frontend | Next.js 16 + Tailwind CSS |
| GPU Runtime | Google Colab T4 |
| Tunnel | ngrok |

---

## Paper

The full IEEE-format conference paper is at `report/legal_nlp_paper.tex`. Open in [Overleaf](https://www.overleaf.com) — paste the file contents into a new project using the `IEEEtran` document class.

---

## Authors

- **Challa Abhiram** — bl.en.u4aie23044@bl.students.amrita.edu
- Dept. of Computer Science & Engineering, Amrita School of Computing, Bengaluru
- Amrita Vishwa Vidyapeetham, India
