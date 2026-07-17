import re

CLAUSES = {
    "indemnity": ["indemnif", "compensat", "make good", "hold harmless"],
    "termination": ["terminat", "cancel", "end of contract", "expiry", "notice period"],
    "arbitration": ["arbitrat", "dispute resolution", "refer to arbitrat"],
    "force_majeure": ["force majeure", "act of god", "beyond control", "unforeseen"],
    "jurisdiction": ["jurisdiction", "court of", "competent court", "shall be tried"],
    "penalty": ["penalty", "liquidated damages", "damages", "fine of"],
    "liability_limit": ["limitation of liability", "shall not be liable", "maximum liability"],
    "confidentiality": ["confidential", "non-disclosure", "shall not disclose", "proprietary"],
    "governing_law": ["governed by", "subject to laws of", "applicable law"],
}

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


class ClauseExtractor:
    """
    Keyword-based clause extractor — runs fully locally without ML models.
    Model-based extraction (roberta-base-squad2) is done in the Colab notebook.
    """

    def extract_clauses(self, text: str) -> dict:
        sentences = SENTENCE_SPLIT.split(text)
        results = {}

        for clause_name, keywords in CLAUSES.items():
            for sentence in sentences:
                sentence_lower = sentence.lower()
                if any(kw in sentence_lower for kw in keywords):
                    results[clause_name] = {
                        "text": sentence.strip(),
                        "confidence": 1.0,  # rule-based — always certain
                        "method": "keyword",
                    }
                    break  # take first matching sentence per clause

        return results
