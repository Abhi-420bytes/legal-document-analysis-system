import pdfplumber
from docx import Document as DocxDocument
import os


class DocumentParser:
    """Parses PDF, DOCX, and plain text legal documents into raw text."""

    SUPPORTED = {".pdf", ".docx", ".txt"}

    def parse(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.SUPPORTED:
            raise ValueError(f"Unsupported file type: {ext}. Use PDF, DOCX, or TXT.")

        if ext == ".pdf":
            return self._parse_pdf(file_path)
        elif ext == ".docx":
            return self._parse_docx(file_path)
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

    def _parse_pdf(self, path: str) -> str:
        text_parts = []
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"--- Page {i + 1} ---\n{page_text}")
        return "\n\n".join(text_parts)

    def _parse_docx(self, path: str) -> str:
        doc = DocxDocument(path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)
