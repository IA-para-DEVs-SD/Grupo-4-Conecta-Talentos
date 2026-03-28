from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "ConectaTalentos"
    debug: bool = False
    secret_key: str = "dev-secret-key"

    database_url: str = "sqlite:///./data/database.db"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_max_tokens: int = 2000

    upload_dir: str = "./data/uploads"
    max_file_size_mb: int = 10
    max_pdf_pages: int = 10

    presidio_language: str = "pt"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
