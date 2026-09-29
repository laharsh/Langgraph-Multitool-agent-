"""
rag_tool.py — call Project 1 RAG API as a knowledge base tool.

Requires rag-eval-platform running: uvicorn src.api:app --port 8000
"""

from __future__ import annotations

import httpx

from src.config import RAG_API_URL


def knowledge_search(question: str, timeout: float = 60.0) -> str:
    """
    POST question to Project 1 /ask and return answer + source labels.

    Returns a plain-text block the agent can cite in its final answer.
    """
    q = question.strip()
    if not q:
        return "Error: empty question"

    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(RAG_API_URL, json={"question": q})
            resp.raise_for_status()
            data = resp.json()
    except httpx.ConnectError:
        return (
            "Error: RAG API not reachable. Start Project 1 first:\n"
            "  cd rag-eval-platform && uvicorn src.api:app --port 8000"
        )
    except httpx.HTTPStatusError as exc:
        return f"Error: RAG API returned {exc.response.status_code}"
    except httpx.HTTPError as exc:
        return f"Error: {exc}"

    answer = data.get("answer", "")
    sources = data.get("sources", [])
    source_lines = [
        f"  - {s.get('source', '?')} (page {s.get('page', '?')})" for s in sources[:5]
    ]
    block = f"Answer: {answer}"
    if source_lines:
        block += "\nSources:\n" + "\n".join(source_lines)
    return block


if __name__ == "__main__":
    print(knowledge_search("What are the four functions in the NIST AI RMF?"))
