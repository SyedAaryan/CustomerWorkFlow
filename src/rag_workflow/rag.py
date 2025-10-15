from src.vector_store.faiss_store import FAISSStore
from src.llm.gemini_client import ask_gemini
from src.config.settings import TOP_K
from src.config.logger import logger


class RAGWorkflow:
    def __init__(self, store: FAISSStore):
        self.store = store

    def execute(self, user_input: str) -> str:
        """
        Executes the RAG workflow for a given user input.
        """
        logger.info(f"Executing RAG workflow for input: '{user_input}'")
        top_chunks = self.store.query(user_input, top_k=TOP_K)
        context = "\n".join(top_chunks)

        prompt = f"""
        You are an AI assistant helping employees understand company policies.
        Use the context to answer clearly and accurately.

        Context:
        {context}

        Question: {user_input}
        """

        answer = ask_gemini(prompt)
        logger.info(f"Generated answer: '{answer.strip()}'")
        return answer
