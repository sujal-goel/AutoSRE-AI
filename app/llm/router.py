# PURPOSE:
# - switch between Gemini and OpenAI

# WHY:
# - flexibility (your requirement)

# LOGIC:
# if USE_GEMINI:
#   use gemini_client
# else:
#   use openai_client

# ONLY CHANGE HERE TO SWITCH MODEL


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