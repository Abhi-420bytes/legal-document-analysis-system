import chromadb
from sentence_transformers import SentenceTransformer


class CaseRetriever:
    COLLECTION_NAME = "legal_cases"

    def __init__(self, db_path: str = "./case_database"):
        self.encoder   = SentenceTransformer("all-MiniLM-L6-v2")
        self.client    = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(self.COLLECTION_NAME)

    def index_cases(self, cases: list[dict]):
        """Index cases. Each dict needs id, text (or summary), case_type."""
        ids, embeddings, documents, metadatas = [], [], [], []
        existing = set(self.collection.get()["ids"])

        for case in cases:
            if case["id"] in existing:
                continue
            body = case.get("text") or case.get("summary", "")
            ids.append(case["id"])
            embeddings.append(self.encoder.encode(body).tolist())
            documents.append(body)
            metadatas.append({
                "title":     case.get("title", ""),
                "court":     case.get("court", ""),
                "year":      str(case.get("year", "")),
                "outcome":   case.get("outcome", ""),
                "sections":  case.get("sections", ""),
                "case_type": case.get("case_type", ""),
            })

        if ids:
            self.collection.add(
                ids=ids, embeddings=embeddings,
                documents=documents, metadatas=metadatas,
            )
        return len(ids)

    def find_similar(self, query_text: str, n: int = 3) -> list[dict]:
        total = self.collection.count()
        if total == 0:
            return []
        emb = self.encoder.encode(query_text).tolist()
        res = self.collection.query(
            query_embeddings=[emb], n_results=min(n, total),
        )
        results = []
        for i, doc in enumerate(res["documents"][0]):
            meta = res["metadatas"][0][i]
            dist = res["distances"][0][i] if res.get("distances") else None
            results.append({
                "title":            meta.get("title", ""),
                "court":            meta.get("court", ""),
                "year":             meta.get("year", ""),
                "outcome":          meta.get("outcome", ""),
                "sections":         meta.get("sections", ""),
                "case_type":        meta.get("case_type", ""),
                "summary":          doc[:300] + "…" if len(doc) > 300 else doc,
                "similarity_score": round(1 - dist, 3) if dist is not None else None,
            })
        return results
