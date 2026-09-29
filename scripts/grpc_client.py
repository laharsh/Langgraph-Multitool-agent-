"""
Demo gRPC client — same question as REST /chat.

Usage:
    python scripts/grpc_client.py "What was Q3 revenue for product Alpha?"
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import grpc

from src.config import GRPC_PORT
from src.grpc_gen import agent_pb2, agent_pb2_grpc


def main() -> None:
    question = " ".join(sys.argv[1:]).strip() or "What was Q3 revenue for product Alpha?"
    target = f"localhost:{GRPC_PORT}"

    with grpc.insecure_channel(target) as channel:
        stub = agent_pb2_grpc.AgentServiceStub(channel)
        response = stub.AskAgent(agent_pb2.AgentRequest(message=question))

    print(f"Question: {question}\n")
    print("Answer:")
    print(response.answer)
    if response.tool_calls:
        print("\nTool calls:")
        for i, tc in enumerate(response.tool_calls, 1):
            args = tc.args_json
            try:
                args = json.loads(tc.args_json)
            except json.JSONDecodeError:
                pass
            print(f"  {i}. {tc.tool}({args})")
            if tc.result:
                preview = tc.result.replace("\n", " ")[:100]
                print(f"     -> {preview}...")


if __name__ == "__main__":
    main()
