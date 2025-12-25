from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "outputs"
    WHISPER_MODEL: str = "small"
    GPT_MODEL: str = "gpt-4"
    MAX_FILE_SIZE: int = 500 * 1024 * 1024  # 500MB
    
    class Config:
        env_file = ".env"

settings = Settings()