# MCP tool server

Exposes the same tools as the LangGraph agent over **Model Context Protocol** (stdio).

## Run

```powershell
cd langgraph-agent
.venv\Scripts\activate
# Terminal 1: P1 RAG
cd ..\rag-eval-platform
uvicorn src.api:app --port 8000

# Terminal 2: MCP server
cd ..\langgraph-agent
python -m src.mcp_tools_server
```

## Cursor / IDE config (example)

```json
{
  "mcpServers": {
    "governance-tools": {
      "command": "C:\\path\\to\\langgraph-agent\\.venv\\Scripts\\python.exe",
      "args": ["-m", "src.mcp_tools_server"],
      "cwd": "C:\\path\\to\\langgraph-agent"
    }
  }
}
```

Tools: `sql_query_tool`, `calculator_tool`, `web_search_tool`, `knowledge_search_tool`.

LangGraph REST/gRPC remain the **orchestration** story; MCP is the **interop** story for tool reuse.
