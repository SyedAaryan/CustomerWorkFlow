# src/email_agent/classifier.py
from src.llm.gemini_client import ask_gemini  # or however you access your model


def classify_email_content(content: str) -> str:
    """
    Classify incoming email content into one of:
    - 'policy_question'
    - 'irrelevant'
    - 'human_escalation'
    """

    prompt = f"""
    You are an intelligent email classifier.
    Categorize the following email into one of:
    - "policy_question" (if the email contains a question about company policy)
    - "irrelevant" (if it's spam, marketing, or unrelated)
    - "human_escalation" (if it's something sensitive, ambiguous, or cannot be auto-answered)

    Email:
    \"\"\"{content}\"\"\"

    Return ONLY one of the labels: policy_question or irrelevant.
    """

    response = ask_gemini(prompt)  # adjust to your model interface
    label = response.strip().lower()

    if label not in ["policy_question", "irrelevant"]:
        label = "irrelevant"

    return label
