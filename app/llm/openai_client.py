
"""
PURPOSE:
- Handle OpenAI API interactions

WHY:
- Required in problem statement (even if using Gemini now)

FEATURES:
- Compatible with inference script
- Easily switchable
"""

from openai import OpenAI
from app.config.settings import settings


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.API_BASE_URL  # supports HF router or OpenAI
        )
        self.model = settings.MODEL_NAME or "gpt-4o-mini"

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[OpenAI Error]: {str(e)}"