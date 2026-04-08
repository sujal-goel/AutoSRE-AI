
"""
PURPOSE:
- Handle all Gemini API interactions

FEATURES:
- Clean wrapper
- Reusable across project
- Handles errors safely
"""

import google.generativeai as genai
from app.config.settings import settings


class GeminiClient:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.MODEL_NAME or "gemini-pro")

    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text if response.text else ""
        except Exception as e:
            return f"[Gemini Error]: {str(e)}"