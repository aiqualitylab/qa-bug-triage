import uuid
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from rank_bm25 import BM25Okapi

_collection = None
_all_bugs   = []

def init_store():
    global _collection, _all_bugs

    client      = chromadb.PersistentClient(path="./chroma_db")
    _collection = client.get_or_create_collection(
        name="bug_reports",
        embedding_function=DefaultEmbeddingFunction()
    )

    data = _collection.get(include=["metadatas"])
    _all_bugs = data["metadatas"] or []

    print(f"[rag] Ready - {len(_all_bugs)} bugs loaded")

def add_bug(bug: dict):
    init_store()

    bug_id = bug.get("bug_id") or f"BUG-{uuid.uuid4().hex[:6].upper()}"
    text = f"{bug.get('title', '')}. {bug.get('description', '')}"

    metadata = {
        "bug_id": bug_id,
        "title": str(bug.get("title", "")),
        "severity": str(bug.get("severity", "unknown")),
        "component": str(bug.get("component", "unknown")),
        "platform": str(bug.get("platform", "unknown")),
        "frequency": str(bug.get("frequency_estimate", "unknown")),
        "description": str(bug.get("description", ""))[:400],
    }

    _collection.upsert(ids=[bug_id], documents=[text], metadatas=[metadata])
    _all_bugs.append(metadata)

def search_bugs(query: str, top_k: int = 5):
    init_store()

    results = _collection.query(query_texts=[query], n_results=top_k)
    sem_bugs = results.get("metadatas", [[]])[0]

    corpus = [f"{bug.get('title', '')}. {bug.get('description', '')}" for bug in _all_bugs]
    bm25 = BM25Okapi(corpus + [""])
    bm25_scores = bm25.get_scores(query.split())
    bm25_indices = sorted(range(len(_all_bugs)), key=lambda i: bm25_scores[i], reverse=True)[:top_k]
    bm25_bugs = [_all_bugs[i] for i in bm25_indices]

    sem_rank = {bug["bug_id"]: idx + 1 for idx, bug in enumerate(sem_bugs)}
    bm25_rank = {bug["bug_id"]: idx + 1 for idx, bug in enumerate(bm25_bugs)}
    bug_by_id = {bug["bug_id"]: bug for bug in sem_bugs + bm25_bugs}
    candidate_ids = set(sem_rank) | set(bm25_rank)

    rrf_k = 60
    default_rank = 10**6
    ranked_ids = sorted(
        candidate_ids,
        key=lambda bug_id: (1 / (rrf_k + sem_rank.get(bug_id, default_rank))) + (1 / (rrf_k + bm25_rank.get(bug_id, default_rank))),
        reverse=True,
    )

    return [bug_by_id[bug_id] for bug_id in ranked_ids[:top_k]]