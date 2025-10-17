import sys
from pathlib import Path
from src.ingestion.file_loader import load_policy_and_create_index
from src.vector_store.faiss_store import FAISSStore
from src.rag_workflow.rag import RAGWorkflow
from src.config.settings import POLICY_FILE
from src.config.logger import logger
from src.email_agent.reader import start_email_agent

import os
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""

# Ensure src is in Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

rag_workflow = None


def setup_rag():
    """
    Initializes the FAISS index and RAG workflow once at startup.
    """
    global rag_workflow
    logger.info("🧠 Initializing FAISS and RAG workflow...")

    store = FAISSStore()
    if store.index is None:
        logger.warning("🧠 FAISS index not found — building now...")
        try:
            load_policy_and_create_index(POLICY_FILE)
            store = FAISSStore()
        except FileNotFoundError as e:
            logger.error(f"Failed to build index: {e}")
            sys.exit(1)
    else:
        logger.info("✅ FAISS index found and loaded!")

    rag_workflow = RAGWorkflow(store)
    return rag_workflow


def start_chatbot():
    """
    Runs the chatbot that answers questions about the company policy.
    """
    global rag_workflow
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


def main():
    """
    Main function to choose between chatbot or email agent.
    """
    # 🧠 Initialize RAG once
    setup_rag()

    # ✅ Then show menu
    print("\n============================")
    print("🤖  AI Assistant Main Menu")
    print("============================")
    print("1. 💬 Ask questions about company policy")
    print("2. 📧 Start Email Agent")
    print("0. ❌ Exit")
    print("============================")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        start_chatbot()
    elif choice == "2":
        start_email_agent(rag_workflow)
    elif choice == "0":
        print("👋 Exiting...")
        sys.exit(0)
    else:
        print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
