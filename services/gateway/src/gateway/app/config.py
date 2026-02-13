from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ingestion_url: str = "http://localhost:8001"
    query_url: str = "http://localhost:8002"
    model: str = "llama3.2:3b"
    qdrant_url: str = "http://localhost:6333"
    ollama_url: str = "http://localhost:11434"

settings = Settings()


