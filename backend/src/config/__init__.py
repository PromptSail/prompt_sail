import os
from pathlib import Path

from dotenv import dotenv_values, find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent


class Config(BaseSettings):
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = "prompt_sail"
    BASE_URL: str = "http://localhost:8000"
    BUILD_SHA: str = "unknown"
    TEMPLATES_DIRECTORY: str = str((BASE_DIR / Path("web/templates")).resolve())
    STATIC_DIRECTORY: str = str((BASE_DIR / Path("../static")).resolve())
    GOOGLE_CLIENT_ID: str | None = os.getenv("GOOGLE_CLIENT_ID", None)
    AZURE_CLIENT_ID: str | None = os.getenv("AZURE_CLIENT_ID", None)
    SSO_AUTH: bool = os.getenv("SSO_AUTH", "False").lower() in ("true", "1", "t")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "PromptSail")


config = Config()

if config.DEBUG:
    print("Using config:", config)
