"""
MCP server exposing governance agent tools (stdio transport).

Run (Project 1 API must be on :8000 for knowledge_search):
    python -m src.mcp_tools_server

Connect from Cursor / Claude Desktop via MCP config pointing to this command.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from src.tools.calculator_tool import calculator
from src.tools.rag_tool import knowledge_search
from src.tools.search_tool import web_search
from src.tools.sql_tool import sql_query

mcp = FastMCP("governance-agent-tools")


@mcp.tool()
def sql_query_tool(query: str) -> str:
    """Read-only SQL on ai_systems, compliance_findings, sales, employees, support_tickets."""
    return sql_query(query)


@mcp.tool()
def calculator_tool(expression: str) -> str:
    """Safe math, e.g. 45000 * 0.18"""
    return calculator(expression)


@mcp.tool()
def web_search_tool(query: str) -> str:
    """Mock internal policy snippets (refund, shipping, warranty)."""
    return web_search(query)


@mcp.tool()
def knowledge_search_tool(question: str) -> str:
    """EU AI Act, NIST AI RMF, India DPDP via Project 1 RAG API."""
    return knowledge_search(question)


if __name__ == "__main__":
    mcp.run()
