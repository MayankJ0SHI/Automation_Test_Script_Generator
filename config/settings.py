from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Set

class Settings(BaseSettings):
    LLM_MODEL: str = "gpt-4-turbo"
    ALLOWED_EXTENSIONS: Set[str] = {'.java', '.xml', '.properties', '.yaml', '.yml'}
    EMBED_MODEL: str = "text-embedding-3-small"
    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 50
    CHROMA_DB: str    = "DB_NAME"
    CHROMA_PERSIST_DIR: str = str(Path(__file__).resolve().parent.parent / "chroma_data")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()