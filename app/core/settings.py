"""Application settings and configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


OLLAMA_BASE_URL = "http://xxxx.a.free.pinggy.link"   # Ollama Pinggy tunnel URL
OLLAMA_MODEL    = "gpt-oss:20b"
INTENT_API_URL  = "http://yyyy.a.free.pinggy.link/predict"  # Intent server Pinggy tunnel URL


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ollama_base_url: str = OLLAMA_BASE_URL
    ollama_model: str = OLLAMA_MODEL
    intent_api_url: str = INTENT_API_URL


settings = Settings()
