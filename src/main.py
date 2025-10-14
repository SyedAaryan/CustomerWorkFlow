import sys
from pathlib import Path

# Ensure src is in Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "src"))

from ingestion.file_loader import load_policy_and_create_index
from vector_store.faiss_store import FAISSStore
from llm.gemini_client import ask_gemini
from config.settings import POLICY_FILE, TOP_K


def main():
    print("\n🚀 Starting AI RAG Chatbot...\n")

    store = FAISSStore()

    if store.index is None:
        print("🧠 FAISS index not found — building now...")
        load_policy_and_create_index(POLICY_FILE)
        store = FAISSStore()  # reload after building
    else:
        print("✅ FAISS index found! Ready to query.\n")

    # Chat loop
    print("💬 Ask questions about the company policy! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        top_chunks = store.query(user_input, top_k=TOP_K)
        context = "\n".join(top_chunks)
        prompt = f"""
        You are an AI assistant helping employees understand company policies.
        Use the context to answer clearly and accurately.

        Context:
        {context}

        Question: {user_input}
        """

        answer = ask_gemini(prompt)
        print(f"\nBot: {answer.strip()}\n")


if __name__ == "__main__":
    main()
