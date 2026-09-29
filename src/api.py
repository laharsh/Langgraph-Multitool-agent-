"""
api.py — FastAPI REST API for the LangGraph agent (Phase 3).

Start:
    uvicorn src.api:app --reload --port 8001

Test:
    curl http://localhost:8001/health
    curl -X POST http://localhost:8001/chat -H "Content-Type: application/json" \\
         -d "{\"message\": \"What was Q3 revenue for Alpha?\"}"
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.agent_service import run_chat
from src.config import API_PORT, LLM_PROVIDER

app = FastAPI(
    title="LangGraph Business & Compliance Agent",
    description="Multi-tool agent: SQL, calculator, mock search, Project 1 RAG",
    version="0.3.0",
)


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=3,
        examples=["What was Q3 revenue for product Alpha?"],
    )


class ToolCallItem(BaseModel):
    tool: str
    args: dict
    result: str | None = None


class ChatResponse(BaseModel):
    message: str
    answer: str
    tool_calls: list[ToolCallItem]


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "llm_provider": LLM_PROVIDER,
        "service": "langgraph-agent",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest) -> ChatResponse:
    """
    Run the agent on a user message.

    Returns the final answer plus a log of every tool invocation (name, args, result).
    """
    try:
        result = run_chat(body.message)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Agent failed: {exc}") from exc

    tool_calls = [
        ToolCallItem(
            tool=tc["tool"],
            args=tc["args"],
            result=tc.get("result"),
        )
        for tc in result["tool_calls"]
    ]
    return ChatResponse(
        message=result["message"],
        answer=result["answer"],
        tool_calls=tool_calls,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.api:app", host="0.0.0.0", port=API_PORT, reload=True)
