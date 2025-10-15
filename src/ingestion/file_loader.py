from pathlib import Path
from src.vector_store.faiss_store import FAISSStore
from src.config.settings import POLICY_FILE
from src.config.logger import logger


def load_policy_and_create_index(policy_path: str = POLICY_FILE):
    """Loads the policy document and creates a FAISS index."""
    logger.info(f"📄 Loading policy document from: {policy_path}")

    policy_file = Path(policy_path)
    if not policy_file.exists():
        logger.error(f"Policy file not found: {policy_path}")
        raise FileNotFoundError(f"Policy file not found: {policy_path}")

    with open(policy_file, "r", encoding="utf-8") as f:
        text = f.read()

    store = FAISSStore()
    store.build_index(text)
    logger.info("✅ Policy file embedded and FAISS index created successfully!\n")
