import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Lexi Cloud")
    api_token: str = os.getenv("APP_TOKEN", "")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "").rstrip("/")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "")
    database_path: str = os.getenv("DATABASE_PATH", "/data/lexi.db")
    max_history_messages: int = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))

settings = Settings()
