from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "langgraph-agent"
    assert "llm_provider" in data


def test_chat_requires_message():
    resp = client.post("/chat", json={"message": "ab"})
    assert resp.status_code == 422


def test_chat_returns_tool_calls(monkeypatch):
    def fake_run(message: str):
        return {
            "message": message,
            "answer": "Total is 100.",
            "tool_calls": [
                {
                    "tool": "sql_query",
                    "args": {"query": "SELECT 1"},
                    "result": "1",
                }
            ],
        }

    monkeypatch.setattr("src.api.run_chat", fake_run)
    resp = client.post("/chat", json={"message": "What is revenue?"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["answer"] == "Total is 100."
    assert len(data["tool_calls"]) == 1
    assert data["tool_calls"][0]["tool"] == "sql_query"
