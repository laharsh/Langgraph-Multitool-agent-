import json
from unittest.mock import MagicMock

from src.grpc_gen import agent_pb2
from src.grpc_server import AgentServicer


def test_grpc_ask_agent(monkeypatch):
    def fake_chat(message: str):
        return {
            "message": message,
            "answer": "8100",
            "tool_calls": [
                {
                    "tool": "calculator",
                    "args": {"expression": "45000*0.18"},
                    "result": "8100",
                }
            ],
        }

    monkeypatch.setattr("src.grpc_server.run_chat", fake_chat)
    servicer = AgentServicer()
    response = servicer.AskAgent(
        agent_pb2.AgentRequest(message="tax on 45000"),
        MagicMock(),
    )
    assert response.answer == "8100"
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0].tool == "calculator"
    assert json.loads(response.tool_calls[0].args_json)["expression"] == "45000*0.18"
