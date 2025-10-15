import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.config.settings import EMBED_MODEL, FAISS_INDEX_FILE, CHUNK_SIZE, CHUNK_OVERLAP
from src.config.logger import logger


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
        logger.info("Building FAISS index...")
        self.chunks = chunk_text(text)
        embeddings = self.model.encode(self.chunks, convert_to_numpy=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)
        self.save_index()
        logger.info(f"[FAISSStore] Indexed {len(self.chunks)} chunks.")

    def save_index(self):
        if self.index is not None:
            faiss.write_index(self.index, FAISS_INDEX_FILE)
            np.save(FAISS_INDEX_FILE + "_chunks.npy", np.array(self.chunks, dtype=object))
            logger.info(f"FAISS index saved to {FAISS_INDEX_FILE}")

    def load_index(self):
        logger.info(f"Loading FAISS index from {FAISS_INDEX_FILE}")
        self.index = faiss.read_index(FAISS_INDEX_FILE)
        self.chunks = np.load(FAISS_INDEX_FILE + "_chunks.npy", allow_pickle=True).tolist()
        logger.info(f"[FAISSStore] Loaded index with {len(self.chunks)} chunks.")

    def query(self, query, top_k=4):
        logger.info(f"Querying FAISS index for: '{query}'")
        q_emb = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(q_emb, top_k)
        retrieved_chunks = [self.chunks[i] for i in I[0]]
        logger.info(f"Retrieved {len(retrieved_chunks)} chunks from FAISS.")
        return retrieved_chunks
