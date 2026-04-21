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