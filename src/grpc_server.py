"""
grpc_server.py — gRPC AgentService (Phase 4).

Start:
    python -m src.grpc_server
"""

from __future__ import annotations

import json
from concurrent import futures

import grpc

from src.agent_service import run_chat, tool_call_args_json
from src.config import GRPC_PORT
from src.grpc_gen import agent_pb2, agent_pb2_grpc


class AgentServicer(agent_pb2_grpc.AgentServiceServicer):
    def AskAgent(self, request, context):  # noqa: N802 — gRPC name
        try:
            result = run_chat(request.message)
        except ValueError as exc:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(exc))
            return agent_pb2.AgentResponse()
        except Exception as exc:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Agent failed: {exc}")
            return agent_pb2.AgentResponse()

        tool_calls = []
        for tc in result["tool_calls"]:
            tool_calls.append(
                agent_pb2.ToolCall(
                    tool=tc["tool"],
                    args_json=tool_call_args_json(tc["args"]),
                    result=tc.get("result") or "",
                )
            )
        return agent_pb2.AgentResponse(
            answer=result["answer"],
            tool_calls=tool_calls,
        )


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    agent_pb2_grpc.add_AgentServiceServicer_to_server(AgentServicer(), server)
    server.add_insecure_port(f"[::]:{GRPC_PORT}")
    server.start()
    print(f"gRPC AgentService listening on port {GRPC_PORT}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
