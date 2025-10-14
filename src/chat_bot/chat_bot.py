from src.llm.gemini_client import ask_gemini


def start_chatbot():
    print("💬 Ask questions about the company policy! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Here you could add FAISS context retrieval later
        answer = ask_gemini(user_input)
        print(f"\nBot: {answer}\n")
