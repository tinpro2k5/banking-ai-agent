"""Ollama client module."""
import requests
from app.clients.base import BaseLLMClient
from app.core.settings import OLLAMA_BASE_URL, OLLAMA_MODEL
from .base import BaseClient


class OllamaClient(BaseLLMClient):
    """Ollama client for LLM interactions."""

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
        )
        return response.json()["response"]
