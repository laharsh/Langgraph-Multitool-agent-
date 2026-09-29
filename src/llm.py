"""Chat model for the agent (must support tool calling)."""

from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel

from src.config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    LLM_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)


def get_chat_model() -> BaseChatModel:
    """
    Return the configured chat LLM with tool-calling support.

    Default is Groq — agent loops need stable tool calls; local Ollama often
    crashes on Windows GPU (CUDA) or weak tool support on 3B models.
    """
    if LLM_PROVIDER == "groq":
        from langchain_groq import ChatGroq

        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY missing in .env")
        kwargs: dict = {
            "model": GROQ_MODEL,
            "api_key": GROQ_API_KEY,
            "temperature": 0,
            "timeout": 120,
            "max_retries": 2,
        }
        if "gpt-oss" in GROQ_MODEL:
            kwargs["reasoning_effort"] = "low"
            kwargs["reasoning_format"] = "hidden"
        return ChatGroq(**kwargs)

    from langchain_ollama import ChatOllama

    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
        num_ctx=4096,
        num_gpu=0,
    )
