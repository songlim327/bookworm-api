from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

# Load config from .env file
load_dotenv(find_dotenv(".env"))

class Settings(BaseSettings):
    ollama_model: str = "llama2"
    ollama_host: str
    ollama_port: int = 11434
    chroma_host: str
    chroma_port: int = 8000
    chroma_auth_credentials: str