from transformers import pipeline as hf_pipeline


CASE_LABELS = [
    "criminal",
    "civil",
    "contract_dispute",
    "family_law",
    "property",
    "constitutional",
    "intellectual_property",
    "labour",
]

# Keyword signals used for rule-based fallback
KEYWORD_MAP = {
    "criminal": ["murder", "theft", "assault", "robbery", "fraud", "ipc", "crpc", "accused", "prosecution", "bail", "fir"],
    "civil": ["damages", "tort", "negligence", "plaintiff", "defendant", "injunction", "decree"],
    "contract_dispute": ["breach", "contract", "agreement", "indemnity", "party", "obligation", "consideration"],
    "family_law": ["divorce", "custody", "marriage", "alimony", "adoption", "maintenance", "matrimonial"],
    "property": ["property", "land", "title", "ownership", "easement", "tenancy", "lease", "rent"],
    "constitutional": ["fundamental rights", "article", "constitution", "writ", "mandamus", "certiorari"],
    "intellectual_property": ["patent", "trademark", "copyright", "infringement", "trade secret"],
    "labour": ["employment", "worker", "salary", "termination", "industrial dispute", "retrenchment"],
}


class CaseTypeClassifier:
    """
    Classifies legal documents by case type using a zero-shot transformer
    with a keyword-based fallback.
    """

    def __init__(self):
        # Zero-shot classification works without fine-tuning
        self._pipeline = hf_pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
        )

    def predict(self, text: str) -> dict:
        snippet = text[:1024]  # keep inference fast

        try:
            result = self._pipeline(snippet, candidate_labels=CASE_LABELS, multi_label=False)
            scores = dict(zip(result["labels"], result["scores"]))
            top_label = result["labels"][0]
            top_score = result["scores"][0]
        except Exception:
            top_label, top_score, scores = self._keyword_fallback(text)

        return {
            "case_type": top_label,
            "confidence": round(top_score, 4),
            "all_scores": {k: round(v, 4) for k, v in scores.items()},
        }

    def _keyword_fallback(self, text: str):
        text_lower = text.lower()
        tally = {label: 0 for label in CASE_LABELS}
        for label, keywords in KEYWORD_MAP.items():
            for kw in keywords:
                tally[label] += text_lower.count(kw)

        sorted_labels = sorted(tally.items(), key=lambda x: x[1], reverse=True)
        total = sum(tally.values()) or 1
        scores = {label: count / total for label, count in tally.items()}
        top_label = sorted_labels[0][0]
        top_score = scores[top_label]
        return top_label, top_score, scores
