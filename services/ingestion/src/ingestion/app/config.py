from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Doc App"
    qdrant_url: str = "http://localhost:6333"
    ollama_url: str = "http://localhost:11434"

settings = Settings()


