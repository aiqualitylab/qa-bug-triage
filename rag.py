import os
import uuid
import chromadb

from llama_index.core import VectorStoreIndex, Document, StorageContext
from llama.index.vector_stores.chroma import ChromaVectorStore
from llama.index.core.retrievers import QueryFusionRetriever
from llama.index.retrievers.bm25 import BM25Retriever
from llama_index.core.node_parser import SentenceSplitter

_index = None
_all_nodes = []

def init_store():
    global _index, _all_nodes
    
    chroma_client     = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = chroma_client.get_or_create_collection("bug_reports")

    vector_store    = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    _index = VectorStoreIndex(nodes=[], storage_context=storage_context)
    _refresh_nodes()

 