# src/gemini_client.py
import google.generativeai as genai
from src.config.settings import GEMINI_API_KEY, GEMINI_MODEL
from src.config.logger import logger  # import your dedicated logger

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


def ask_gemini(prompt: str) -> str:
    """
    Sends a text prompt to the Gemini API and returns the response.
    All debug/info messages are logged to a file.
    """
    logger.debug(f"Sending prompt to Gemini: '{prompt}'")
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)

        # Extract the text from the first candidate
        if response.candidates and response.candidates[0].content.parts:
            generated_text = response.candidates[0].content.parts[0].text
            if generated_text:
                logger.debug("Gemini returned valid text.")
                return generated_text

        logger.debug("Gemini returned no valid response.")
        return "I'm sorry, I cannot generate a response for that."

    except Exception as e:
        logger.error(f"[Gemini] API error: {e}")
        return "I'm having trouble connecting to Gemini right now."
