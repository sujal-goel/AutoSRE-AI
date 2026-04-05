"""
PURPOSE:
- Load all environment variables from .env file

WHY (important for hackathon):
- Problem requires API keys and config variables
- Keeps secrets safe (no hardcoding)
- Used by LLM (Gemini / OpenAI), API, inference

WHAT THIS FILE DOES:
- Reads .env file
- Stores values in one place
- Other files import from here

USAGE:
from app.config.settings import settings
print(settings.GEMINI_API_KEY)
"""

from pydantic import BaseSettings


class Settings(BaseSettings):

    # 🔑 LLM API KEYS
    # Used for calling Gemini / OpenAI
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # 🔁 SWITCH CONTROL
    # True → Gemini
    # False → OpenAI
    USE_GEMINI: bool = True

    # 🤖 MODEL CONFIG
    # Model name used in LLM calls
    MODEL_NAME: str = ""

    # 🌐 API BASE URL
    # Used in OpenAI client / HF router
    API_BASE_URL: str = ""

    # 🔐 HUGGINGFACE TOKEN
    # Required by problem statement
    HF_TOKEN: str = ""

    class Config:
        # tells pydantic to read from .env file
        env_file = ".env"


# ✅ Create global settings object
settings = Settings()