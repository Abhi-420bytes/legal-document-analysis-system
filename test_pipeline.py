"""
Smoke test — runs the full pipeline on a sample legal text.
Run: python test_pipeline.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

SAMPLE_TEXT = """
IN THE HIGH COURT OF DELHI AT NEW DELHI
Civil Suit No. 1234 of 2023

Between:
    ABC Constructions Pvt. Ltd.        ... Plaintiff
    Represented by its Director, Mr. Rajesh Kumar

    AND

    XYZ Developers Ltd.                ... Defendant
    Represented by its MD, Ms. Priya Sharma

Date of Filing: 15th January 2023

PLAINT

1. The Plaintiff entered into a contract dated 10th March 2022 with the Defendant
   for construction of residential apartments at Plot No. 45, Sector 18, Noida,
   Uttar Pradesh for a consideration of Rs. 2,50,00,000/- (Rupees Two Crore Fifty Lakhs).

2. The Defendant breached the contract by failing to make payment of Rs. 75,00,000/-
   (Rupees Seventy Five Lakhs) due on 30th September 2022.

3. The Plaintiff seeks compensation under Section 73 of the Indian Contract Act, 1872
   and an injunction restraining the Defendant from alienating the property.

4. Similar cases: AIR 2019 SC 1456, SCC 2020 Del 789
"""


def main():
    print("=" * 60)
    print("LEGAL ANALYSIS PIPELINE — SMOKE TEST")
    print("=" * 60)

    # 1. NER
    print("\n[1] Named Entity Recognition")
    from backend.pipeline.ner_pipeline import LegalNER
    ner = LegalNER()
    entities = ner.extract_entities(SAMPLE_TEXT)
    for key, vals in entities.items():
        if vals:
            print(f"  {key}: {vals}")

    # 2. Case Type Classification
    print("\n[2] Case Type Classification")
    from backend.pipeline.classifier import CaseTypeClassifier
    clf = CaseTypeClassifier()
    result = clf.predict(SAMPLE_TEXT)
    print(f"  Detected: {result['case_type']} (confidence: {result['confidence']})")

    # 3. Clause Extraction
    print("\n[3] Clause Extraction")
    from backend.pipeline.clause_extractor import ClauseExtractor
    extractor = ClauseExtractor()
    clauses = extractor.extract_clauses(SAMPLE_TEXT)
    for clause, info in clauses.items():
        print(f"  {clause}: \"{info['text']}\" (score: {info['confidence']})")

    # 4. Legal Sections
    print("\n[4] Applicable Legal Sections")
    from backend.data.legal_sections_db import get_sections_for_case_type
    sections = get_sections_for_case_type(result["case_type"])
    for s in sections[:4]:
        print(f"  {s['act']} Sec {s['section']}: {s['title']}")

    # 5. Similar Case Retrieval (empty DB — shows empty result)
    print("\n[5] Similar Cases (DB is empty — will be empty until cases are indexed)")
    from backend.pipeline.case_retriever import CaseRetriever
    retriever = CaseRetriever(db_path="./case_database")
    similar = retriever.find_similar(SAMPLE_TEXT[:300])
    print(f"  Found {len(similar)} similar cases")

    print("\n" + "=" * 60)
    print("ALL PIPELINE COMPONENTS WORKING")
    print("=" * 60)


if __name__ == "__main__":
    main()
