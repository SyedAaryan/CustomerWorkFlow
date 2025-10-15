import sys
from pathlib import Path

# Ensure src is in Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from src.ingestion.file_loader import load_policy_and_create_index
from src.vector_store.faiss_store import FAISSStore
from src.rag_workflow.rag import RAGWorkflow
from src.config.settings import POLICY_FILE
from src.config.logger import logger


def main():
    """
    Main function to initialize and run the RAG Chatbot.
    """
    logger.info("🚀 Starting AI RAG Chatbot...")

    store = FAISSStore()

    if store.index is None:
        logger.warning("🧠 FAISS index not found — building now...")
        try:
            load_policy_and_create_index(POLICY_FILE)
            store = FAISSStore()  # Reload after building
        except FileNotFoundError as e:
            logger.error(f"Failed to build index: {e}")
            return  # Exit if policy file is not found
    else:
        logger.info("✅ FAISS index found! Ready to query.")

    # Initialize the RAG workflow
    rag_workflow = RAGWorkflow(store)

    # --- Start Chatbot Loop ---
    print("\n💬 Ask questions about the company policy! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        if not user_input:
            continue

        answer = rag_workflow.execute(user_input)
        print(f"\nBot: {answer.strip()}\n")


if __name__ == "__main__":
    main()
