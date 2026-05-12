from openai import AsyncOpenAI
import httpx
from src.config import settings

class LLMClient:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        if self.provider == "openai":
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
        elif self.provider == "ollama":
            self.base_url = settings.OLLAMA_BASE_URL
            self.model = settings.OLLAMA_MODEL
            self.client = httpx.AsyncClient()
        else:
            raise ValueError(f"Unknown LLM Provider: {self.provider}")

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends a query to the configured LLM and returns the text response.
        """
        if self.provider == "openai":
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0 # Deterministic parsing
            )
            return response.choices[0].message.content
            
        elif self.provider == "ollama":
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.0
                }
            }
            response = await self.client.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
