from pathlib import Path
from src.vector_store.faiss_store import FAISSStore
from src.config.settings import POLICY_FILE


def load_policy_and_create_index(policy_path: str = POLICY_FILE):
    print("📄 Loading policy document from:", policy_path)

    policy_file = Path(policy_path)
    if not policy_file.exists():
        raise FileNotFoundError(f"Policy file not found: {policy_path}")

    with open(policy_file, "r", encoding="utf-8") as f:
        text = f.read()

    store = FAISSStore()
    store.build_index(text)
    print("✅ Policy file embedded and FAISS index created successfully!\n")
