"""Shared agent invocation for REST, gRPC, and benchmark."""

from __future__ import annotations

import json
from typing import Any

from src.agent_graph import run_agent


def run_chat(message: str) -> dict[str, Any]:
    """
    Run the agent and return a transport-neutral payload.

    Keys: message, answer, tool_calls (list of dicts with tool, args, result).
    """
    text = message.strip()
    if len(text) < 3:
        raise ValueError("message must be at least 3 characters")

    result = run_agent(text)
    tool_calls = []
    for tc in result.get("tool_calls", []):
        tool_calls.append(
            {
                "tool": tc.get("tool", ""),
                "args": tc.get("args") or {},
                "result": tc.get("result"),
            }
        )
    return {
        "message": text,
        "answer": result.get("answer", ""),
        "tool_calls": tool_calls,
    }


def tool_call_args_json(args: dict) -> str:
    return json.dumps(args, ensure_ascii=False)
