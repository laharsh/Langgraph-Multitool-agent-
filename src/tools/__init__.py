"""Agent tools — lazy exports so `python -m src.tools.sql_tool` does not double-import."""

from __future__ import annotations

from typing import Any

__all__ = ["sql_query", "calculator", "web_search", "knowledge_search"]


def __getattr__(name: str) -> Any:
    if name == "sql_query":
        from src.tools.sql_tool import sql_query

        return sql_query
    if name == "calculator":
        from src.tools.calculator_tool import calculator

        return calculator
    if name == "web_search":
        from src.tools.search_tool import web_search

        return web_search
    if name == "knowledge_search":
        from src.tools.rag_tool import knowledge_search

        return knowledge_search
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
