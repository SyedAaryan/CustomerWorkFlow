from src.security.security import gem_ai_key

# Gemini API key
GEMINI_API_KEY = gem_ai_key
GEMINI_MODEL = "gemini-2.5-flash-lite"

# File paths
POLICY_FILE = "data/company_policy.txt"
FAISS_INDEX_FILE = "data/faiss_index.index"  # using .index instead of .pkl

# Chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200

# Embedding model (offline-ready)
EMBED_MODEL = "paraphrase-MiniLM-L3-v2"

# Number of chunks to retrieve for a query
TOP_K = 4
