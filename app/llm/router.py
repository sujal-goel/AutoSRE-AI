

"""
PURPOSE:
- Central switch to choose LLM provider (Gemini / OpenAI)

HOW TO USE:
- Change USE_GEMINI in .env
- No need to modify any other file
"""

from app.config.settings import settings

def get_llm():
    if settings.USE_GEMINI:
        from app.llm.gemini_client import GeminiClient
        return GeminiClient()
    else:
        from app.llm.openai_client import OpenAIClient
        return OpenAIClient()