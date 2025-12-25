"""Application configuration."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "Lead Scoring Agent"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./leads.db"

    llm_provider: str = "ollama"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-sonnet-20240229"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    llamacpp_model_path: Optional[str] = None
    llamacpp_n_ctx: int = 4096

    chroma_persist_dir: str = "./chroma_db"

    clearbit_api_key: Optional[str] = None
    hubspot_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
