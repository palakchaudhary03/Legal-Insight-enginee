from functools import lru_cache
from sentence_transformers import SentenceTransformer
from backend.app.config import MODEL
@lru_cache(maxsize=1)
def model(): return SentenceTransformer(MODEL)
def embed(texts): return model().encode(texts,normalize_embeddings=True,show_progress_bar=False)
