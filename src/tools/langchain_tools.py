"""LangChain @tool wrappers — used by LangGraph agent node."""

from __future__ import annotations

from langchain_core.tools import tool

from src.tools.calculator_tool import calculator as _calculator
from src.tools.rag_tool import knowledge_search as _knowledge_search
from src.tools.search_tool import web_search as _web_search
from src.tools.sql_tool import sql_query as _sql_query


@tool
def sql_query(query: str) -> str:
    """
    Run a read-only SQL SELECT on the company SQLite database.

    Tables:
      - ai_systems(id, name, risk_tier, primary_framework, owner_department)
      - compliance_findings(id, framework, quarter, severity, status, summary)
      - sales(id, quarter, product, revenue, units)
      - employees(id, name, department, hire_date)
      - support_tickets(id, topic, status, created_at)

    Only SELECT statements are allowed.
    """
    return _sql_query(query)


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression. Example: '45000 * 0.18'."""
    return _calculator(expression)


@tool
def web_search(query: str) -> str:
    """Mock web search for company policies (refund, shipping, warranty, support)."""
    return _web_search(query)


@tool
def knowledge_search(question: str) -> str:
    """
    Search AI governance regulations (EU AI Act, NIST AI RMF, India DPDP)
    via the Project 1 RAG API. Requires rag-eval-platform on port 8000.
    """
    return _knowledge_search(question)


AGENT_TOOLS = [sql_query, calculator, web_search, knowledge_search]
