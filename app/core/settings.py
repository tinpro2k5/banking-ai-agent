"""Application settings and configuration."""

OLLAMA_BASE_URL = "http://xxxx.a.free.pinggy.link"  
OLLAMA_MODEL = "gpt-oss-20b"
INTENT_MODEL_PATH = "./intent_model"  # path to your Lab 2 checkpoint

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # App
    app_name: str = "Banking AI Agent"
    debug: bool = False

    # Ollama
    ollama_base_url: str = OLLAMA_BASE_URL
    ollama_model: str = OLLAMA_MODEL

    intent_model_path: str = INTENT_MODEL_PATH

    # Server
    host: str = "0.0.0.0"
    port: int = 6636

    class Config:
        """Settings configuration."""

        env_file = ".env"


settings = Settings()
