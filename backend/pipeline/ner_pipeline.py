import re
import spacy
from transformers import pipeline as hf_pipeline


class LegalNER:
    """Extracts named entities from legal documents."""

    # Regex patterns for legal-specific references
    SECTION_PATTERN = re.compile(
        r"[Ss]ection[s]?\s+\d+[A-Z]?(?:\(\d+\))?(?:\s+of\s+[\w\s]+(?:Act|Code|IPC|CrPC|CPC|IEA))?",
        re.IGNORECASE,
    )
    CASE_CITATION = re.compile(
        r"(?:AIR|SCC|SCR|All|Bom|Cal|Mad|Del|SC|HC)\s+\d{4}\s+\w+\s+\d+",
        re.IGNORECASE,
    )
    MONEY_PATTERN = re.compile(r"(?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d{1,2})?(?:\s*(?:lakh|crore|thousand))?", re.IGNORECASE)

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text: str) -> dict:
        doc = self.nlp(text[:100000])  # spaCy limit guard

        entities = {
            "persons": [],
            "organizations": [],
            "dates": [],
            "locations": [],
            "legal_sections": [],
            "case_citations": [],
            "monetary_amounts": [],
        }

        seen = {k: set() for k in entities}

        for ent in doc.ents:
            val = ent.text.strip()
            if ent.label_ == "PERSON" and val not in seen["persons"]:
                entities["persons"].append(val)
                seen["persons"].add(val)
            elif ent.label_ == "ORG" and val not in seen["organizations"]:
                entities["organizations"].append(val)
                seen["organizations"].add(val)
            elif ent.label_ == "DATE" and val not in seen["dates"]:
                entities["dates"].append(val)
                seen["dates"].add(val)
            elif ent.label_ in ("GPE", "LOC") and val not in seen["locations"]:
                entities["locations"].append(val)
                seen["locations"].add(val)

        # Legal-specific extractions via regex
        for match in self.SECTION_PATTERN.finditer(text):
            val = match.group().strip()
            if val not in seen["legal_sections"]:
                entities["legal_sections"].append(val)
                seen["legal_sections"].add(val)

        for match in self.CASE_CITATION.finditer(text):
            val = match.group().strip()
            if val not in seen["case_citations"]:
                entities["case_citations"].append(val)
                seen["case_citations"].add(val)

        for match in self.MONEY_PATTERN.finditer(text):
            val = match.group().strip()
            if val not in seen["monetary_amounts"]:
                entities["monetary_amounts"].append(val)
                seen["monetary_amounts"].add(val)

        return entities
