"""
Structured database of Indian legal sections.
Extend this with more acts and sections as needed.
"""

LEGAL_SECTIONS: dict = {
    "IPC": {
        "302": {
            "title": "Punishment for murder",
            "description": "Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine.",
            "punishment": "Death or life imprisonment + fine",
            "applies_to": ["murder", "homicide", "killing", "death"],
        },
        "304": {
            "title": "Punishment for culpable homicide not amounting to murder",
            "description": "Culpable homicide where the act is done with the intention of causing death but circumstances reduce it below murder.",
            "punishment": "Up to 10 years imprisonment or life + fine",
            "applies_to": ["culpable homicide", "manslaughter"],
        },
        "376": {
            "title": "Punishment for rape",
            "description": "Whoever commits rape shall be punished with rigorous imprisonment of either description for a term which shall not be less than ten years.",
            "punishment": "Minimum 10 years, may extend to life imprisonment + fine",
            "applies_to": ["rape", "sexual assault"],
        },
        "420": {
            "title": "Cheating and dishonestly inducing delivery of property",
            "description": "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property.",
            "punishment": "Up to 7 years imprisonment + fine",
            "applies_to": ["fraud", "cheating", "misrepresentation", "deception"],
        },
        "406": {
            "title": "Punishment for criminal breach of trust",
            "description": "Whoever commits criminal breach of trust shall be punished with imprisonment up to 3 years, or fine, or both.",
            "punishment": "Up to 3 years imprisonment + fine",
            "applies_to": ["breach of trust", "misappropriation", "embezzlement"],
        },
        "498A": {
            "title": "Husband or relative of husband subjecting woman to cruelty",
            "description": "Cruelty by husband or his relatives towards a married woman.",
            "punishment": "Up to 3 years imprisonment + fine",
            "applies_to": ["domestic violence", "dowry harassment", "cruelty", "matrimonial"],
        },
    },
    "CPC": {
        "9": {
            "title": "Courts to try all civil suits unless barred",
            "description": "The courts shall have jurisdiction to try all suits of a civil nature.",
            "applies_to": ["civil suit", "civil jurisdiction"],
        },
        "89": {
            "title": "Settlement of disputes outside the court",
            "description": "Where it appears to the court that there exist elements of a settlement, the court shall formulate terms and refer to ADR.",
            "applies_to": ["mediation", "arbitration", "settlement", "adr"],
        },
    },
    "Contract_Act": {
        "73": {
            "title": "Compensation for loss or damage caused by breach of contract",
            "description": "When a contract has been broken, the party who suffers from such breach is entitled to receive compensation for any loss.",
            "applies_to": ["breach of contract", "damages", "compensation", "contract"],
        },
        "74": {
            "title": "Compensation for breach of contract where penalty stipulated",
            "description": "When a contract has been broken, if a sum is named as penalty, the party complaining of breach is entitled to receive reasonable compensation.",
            "applies_to": ["penalty clause", "liquidated damages", "breach"],
        },
    },
    "Evidence_Act": {
        "65B": {
            "title": "Admissibility of electronic records",
            "description": "Electronic records are admissible as evidence if conditions in this section are met.",
            "applies_to": ["electronic evidence", "digital records", "cyber"],
        },
    },
}


CASE_TYPE_TO_ACTS = {
    "criminal": ["IPC", "CrPC", "Evidence_Act"],
    "civil": ["CPC", "Evidence_Act"],
    "contract_dispute": ["Contract_Act", "CPC", "Evidence_Act"],
    "family_law": ["IPC", "CPC"],
    "property": ["CPC", "Contract_Act"],
    "constitutional": ["CPC"],
    "intellectual_property": ["CPC"],
    "labour": ["CPC"],
}


def get_sections_for_case_type(case_type: str) -> list[dict]:
    """Return all sections relevant to a given case type."""
    relevant_acts = CASE_TYPE_TO_ACTS.get(case_type, [])
    results = []
    for act in relevant_acts:
        sections = LEGAL_SECTIONS.get(act, {})
        for section_num, info in sections.items():
            results.append({
                "act": act,
                "section": section_num,
                **info,
            })
    return results


def match_sections_to_keywords(keywords: list[str]) -> list[dict]:
    """Find sections whose applies_to list overlaps with the given keywords."""
    keywords_lower = [k.lower() for k in keywords]
    matches = []
    for act, sections in LEGAL_SECTIONS.items():
        for section_num, info in sections.items():
            applies = [a.lower() for a in info.get("applies_to", [])]
            if any(kw in applies for kw in keywords_lower):
                matches.append({"act": act, "section": section_num, **info})
    return matches
