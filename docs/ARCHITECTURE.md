# Architecture — Governance operations agent

Part of the **AI Governance Platform** (see [P1_P2_PRODUCT_STORY.md](../../projects-plan/P1_P2_PRODUCT_STORY.md)).

## Flow

1. User sends a message (CLI, REST `/chat`, gRPC `AskAgent`, or MCP client).
2. **LangGraph** runs an `agent` node (LLM with bound tools).
3. If the LLM requests tools, the **tools** node runs them and loops back (max 5 cycles).
4. Final answer + **tool_calls** log are returned.

## Tools

| Tool | Backend |
|------|---------|
| `sql_query` | SQLite — `ai_systems`, `compliance_findings`, demo `sales` |
| `calculator` | Safe AST math |
| `web_search` | Mock internal policy snippets |
| `knowledge_search` | HTTP → Project 1 `POST /ask` (EU / NIST / DPDP) |

## Ports

| Service | Port |
|---------|------|
| Project 1 RAG | 8000 |
| This agent REST | 8001 |
| This agent gRPC | 50051 |

## Files

- `src/agent_graph.py` — graph definition
- `src/agent_service.py` — shared `run_chat` for REST/gRPC/benchmark
- `src/api.py` — FastAPI
- `src/grpc_server.py` — gRPC
