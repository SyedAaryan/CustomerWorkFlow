import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.config.settings import EMBED_MODEL, FAISS_INDEX_FILE, CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Sliding-window text chunking."""
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    step = chunk_size - overlap
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        start += step
    return chunks


class FAISSStore:
    def __init__(self):
        self.model = SentenceTransformer(EMBED_MODEL)
        self.index = None
        self.chunks = []

        if os.path.exists(FAISS_INDEX_FILE):
            self.load_index()

    def build_index(self, text):
        self.chunks = chunk_text(text)
        embeddings = self.model.encode(self.chunks, convert_to_numpy=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        self.save_index()
        print(f"[FAISSStore] Indexed {len(self.chunks)} chunks.")

    def save_index(self):
        if self.index is not None:
            faiss.write_index(self.index, FAISS_INDEX_FILE)
            np.save(FAISS_INDEX_FILE + "_chunks.npy", np.array(self.chunks, dtype=object))

    def load_index(self):
        self.index = faiss.read_index(FAISS_INDEX_FILE)
        self.chunks = np.load(FAISS_INDEX_FILE + "_chunks.npy", allow_pickle=True).tolist()
        print(f"[FAISSStore] Loaded index with {len(self.chunks)} chunks.")

    def query(self, query, top_k=4):
        q_emb = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(q_emb, top_k)
        return [self.chunks[i] for i in I[0]]
