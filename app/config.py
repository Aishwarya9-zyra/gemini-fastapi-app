import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    APP_NAME: str = "Gemini AI Hub"
    APP_VERSION: str = "1.0.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")

    # Available Gemini models
    AVAILABLE_MODELS: list[str] = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]

settings = Settings()
