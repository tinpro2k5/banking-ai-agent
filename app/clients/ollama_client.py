"""Ollama client module."""
import requests
from app.clients.base import BaseLLMClient
from app.core.settings import settings


class OllamaClient(BaseLLMClient):
    """Ollama client for LLM interactions."""

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{settings.ollama_base_url}/api/generate",
            json={"model": settings.ollama_model, "prompt": prompt, "stream": False}
        )
        return response.json()["response"]
