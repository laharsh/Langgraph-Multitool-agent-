"""Load settings from .env — one place for all config."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

DATA_DIR = ROOT / "data"
DB_PATH = Path(os.getenv("DB_PATH", str(DATA_DIR / "company.db")))

# Default groq: small Ollama models + tool calling often fail; P1 can still use Ollama for RAG.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

RAG_API_URL = os.getenv("RAG_API_URL", "http://localhost:8000/ask")
API_PORT = int(os.getenv("API_PORT", "8001"))
GRPC_PORT = int(os.getenv("GRPC_PORT", "50051"))
MAX_AGENT_LOOPS = int(os.getenv("MAX_AGENT_LOOPS", "5"))


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
