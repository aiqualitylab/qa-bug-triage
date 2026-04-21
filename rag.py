import os
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

    print(f"[rag] Ready — {len(_all_bugs)} bugs loaded")

def add_bug(bug: dict):
       if _collection is None:
        init_store()

        bug_id = bug.get("bug_id") or f"BUG-{uuid.uuid4().hex[:6].upper()}"

        text = f"{bug.get('title', '')}. {bug.get('description', '')}"

        metadata = {
            "bug_id":      bug_id,
            "title":       str(bug.get("title",              "")),
            "severity":    str(bug.get("severity",           "unknown")),
            "component":   str(bug.get("component",          "unknown")),
            "platform":    str(bug.get("platform",           "unknown")),
            "frequency":   str(bug.get("frequency_estimate", "unknown")),
            "description": str(bug.get("description",        ""))[:400],
        }

        _collection.upsert(ids=[bug_id], documents=[text], metadatas=[metadata])
        _all_bugs.append(metadata)
