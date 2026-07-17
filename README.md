# ⚖️ Multi-Domain Legal Document Analysis & Clause Identification System

> AI-powered Legal NLP system for analyzing Indian legal documents using Transformer models, Zero-shot Classification, Retrieval-Augmented Generation (RAG), Named Entity Recognition, Clause Identification, and Summarization.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![Next.js](https://img.shields.io/badge/Next.js-Frontend-black)
![License](https://img.shields.io/badge/License-MIT-success)

---

# 📖 Overview

Legal professionals spend considerable time analyzing lengthy legal documents such as court judgments, contracts, petitions, FIRs, and affidavits. Manual analysis is slow, expensive, and prone to human error.

This project presents an **AI-powered Legal Document Analysis System** that automates legal document understanding using modern Transformer-based Natural Language Processing techniques.

The framework supports:

- Multi-domain legal document classification
- Named Entity Recognition (NER)
- Clause Identification
- Extractive & Abstractive Summarization
- Retrieval-Augmented Generation (RAG)
- Relevant precedent retrieval
- Applicable legal section identification

The system is designed specifically for **Indian legal documents** and supports PDF, DOCX, and TXT formats.

---

# 🎯 Objectives

- Automate legal document understanding
- Classify Indian legal cases into multiple legal domains
- Extract legal clauses automatically
- Identify legal entities and statutes
- Generate concise legal summaries
- Recommend similar precedent cases
- Build an intelligent legal assistant

---

# ⚖️ Legal Domains Supported

- Criminal Law
- Civil Law
- Contract Law
- Family Law
- Property Law
- Constitutional Law
- Intellectual Property
- Labour Law

---

# 🚀 Features

- Transformer-based Zero-shot Classification
- Named Entity Recognition (NER)
- Clause Extraction
- Legal Section Detection
- Extractive Summarization
- Claude AI Summarization Support
- Retrieval-Augmented Generation (RAG)
- BM25 Search Engine
- ChromaDB Vector Database
- Semantic Search
- FastAPI Backend
- React / Next.js Frontend
- PDF, DOCX and TXT Support

---

# 🏗️ System Architecture

```
Legal Document
(PDF / DOCX / TXT)
          │
          ▼
Document Parsing
          │
          ▼
Text Preprocessing
          │
          ▼
────────────────────────────────
Parallel Processing
────────────────────────────────

• Zero-shot Classification

• Named Entity Recognition

• Clause Identification

• Summarization

────────────────────────────────
          │
          ▼
Retrieval-Augmented Generation
(BM25 + ChromaDB)
          │
          ▼
Applicable Legal Sections
          │
          ▼
JSON Response
          │
          ▼
Next.js Dashboard
```

---

# 📂 Project Structure

```
legal-document-analysis-system
│
├── backend
│   ├── app.py
│   ├── classifier.py
│   ├── ner.py
│   ├── clause_extractor.py
│   ├── summarizer.py
│   ├── rag.py
│   ├── sections.py
│
├── frontend
│   ├── components
│   ├── pages
│   ├── public
│
├── dataset
│   ├── indian_cases
│
├── vector_store
│
├── models
│
├── requirements.txt
│
└── README.md
```

---

# 🧠 AI Models Used

## Zero-shot Classification

- BART-large-MNLI

Used for multi-class legal document classification without requiring labeled training data.

---

## Secondary Model

- DeBERTa-v3

Used for performance comparison.

---

## Future Fine-tuning

- InLegalBERT

Optimized specifically for Indian legal language.

---

# 🔍 Named Entity Recognition

The system extracts:

- Person
- Organization
- Date
- Money
- Case Number
- Legal Sections
- IPC References
- Citations

using spaCy along with custom legal rules.

---

# 📑 Clause Identification

Automatically identifies important legal clauses including:

- Confidentiality
- Termination
- Force Majeure
- Arbitration
- Penalty
- Indemnity
- Liability

---

# 📚 Retrieval-Augmented Generation (RAG)

The RAG module retrieves similar precedent cases using:

- BM25
- ChromaDB
- MiniLM Sentence Embeddings

instead of relying solely on keyword search.

---

# 📖 Summarization

Supports:

- Claude AI Summarization
- Extractive Summarization (Offline)

Generated summaries include:

- Parties
- Legal Issue
- Key Facts
- Relief Sought
- Applicable Sections

---

# ⚙️ Technology Stack

| Layer | Technology |
|---------|------------|
| Backend | FastAPI |
| Frontend | Next.js |
| Classification | BART-large-MNLI |
| NER | spaCy |
| Embeddings | MiniLM |
| Vector Database | ChromaDB |
| Search | BM25 |
| Summarization | Claude API |
| Language | Python |

---

# 📊 Dataset

The system was evaluated on:

- 80 curated Indian legal cases
- 8 legal domains
- Supreme Court Judgments
- High Court Judgments

---

# 📈 Performance

## Classification Accuracy

| Model | Accuracy |
|---------|-----------|
| BART-large-MNLI | **87.5%** |
| DeBERTa-v3 | 72.5% |
| Fine-tuned InLegalBERT (Target) | 92–95% |

---

## Retrieval Performance

| Metric | Without RAG | With RAG |
|----------|-------------|-----------|
| Match@1 | 88.7% | **100%** |
| Precision@3 | 88.7% | **100%** |
| MRR | 88.7% | **100%** |

---

# 🚀 Installation

Clone repository

```bash
git clone https://github.com/yourusername/legal-document-analysis-system.git

cd legal-document-analysis-system
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Run Backend

```bash
uvicorn app:app --reload
```

---

# ▶ Run Frontend

```bash
npm install

npm run dev
```

---

# 📄 Supported Document Types

- PDF
- DOCX
- TXT

---

# 📊 Output

The system returns:

- Case Category
- Confidence Score
- Named Entities
- Clause List
- Applicable Sections
- Summary
- Top-3 Similar Cases

---

# 🌍 Applications

- Law Firms
- Courts
- Legal Research
- Contract Review
- Government Organizations
- Legal Chatbots
- Judicial Decision Support
- E-Discovery
- Legal Education

---

# 🔮 Future Work

- Fine-tune InLegalBERT
- Multilingual Support (Hindi & Regional Languages)
- Citation Graph Construction
- Legal Question Answering
- Outcome Prediction
- Larger Indian Legal Corpus
- Knowledge Graph Integration
- OCR for Scanned Documents

---

# 📄 Publication

This work was presented as:

**Multi-Domain Legal Document Context Analysis and Clause Identification System Using Transformer-Based Models**

---

# 🌟 Research Highlights

- Transformer-based Legal NLP
- Zero-shot Classification
- Retrieval-Augmented Generation
- Named Entity Recognition
- Clause Identification
- Legal Summarization
- FastAPI + Next.js Deployment
- Semantic Search using ChromaDB
- 87.5% Zero-shot Classification Accuracy
- 100% Match@1 Retrieval with RAG

---

# 👨‍💻 Authors

**Challa Abhiram**

B.Tech Artificial Intelligence Engineering

Amrita School of Computing

Amrita Vishwa Vidyapeetham

---

**Shilpita Vankayala**

Amrita School of Computing

---

**Mukkeshh V**

Amrita School of Computing

---

# 🙏 Acknowledgement

We thank **Amrita Vishwa Vidyapeetham** for providing the academic environment and guidance to conduct this research in Legal Natural Language Processing.

---

# 📜 License

This project is intended for academic research and educational purposes.

Feel free to fork, improve, and cite the work.

⭐ If you find this repository useful, consider giving it a star!
