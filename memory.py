# memory.py
import chromadb
from sentence_transformers import SentenceTransformer
import time

client = chromadb.PersistentClient(path="./max_memory")
collection = client.get_or_create_collection("conversations")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

_cache = {}

def save_memory(user_input: str, ai_response: str):
    try:
        text = f"User: {user_input}\nMAX: {ai_response}"
        embedding = embedder.encode(text, show_progress_bar=False).tolist()
        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[str(time.time())]
        )
    except Exception as e:
        print(f"[MEMORY] Save error: {e}")

def recall_memory(query: str, n: int = 2) -> str:
    try:
        if collection.count() == 0:
            return ""
        if query in _cache:
            return _cache[query]
        embedding = embedder.encode(query, show_progress_bar=False).tolist()
        results = collection.query(
            query_embeddings=[embedding],
            n_results=min(n, collection.count())
        )
        result = "\n".join(results["documents"][0])
        _cache[query] = result
        return result
    except Exception as e:
        print(f"[MEMORY] Recall error: {e}")
        return ""