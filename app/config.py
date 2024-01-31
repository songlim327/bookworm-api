# import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv 

class Settings(BaseSettings):
    ollama_model: str = "llama2"
    ollama_host: str
    ollama_port: int = 11434
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
# OLLAMA_HOST = os.getenv("OLLAMA_HOST")
# OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")

# Load config from .env file
load_dotenv()

config = Settings()