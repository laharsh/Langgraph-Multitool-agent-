"""
search_tool.py — mock web search (no paid API).

Returns canned snippets keyed by topic keywords.
"""

from __future__ import annotations

MOCK_RESULTS: dict[str, str] = {
    "refund": (
        "Refund policy: customers may return products within 30 days of delivery "
        "for a full refund if items are unused and in original packaging."
    ),
    "shipping": (
        "Shipping: standard delivery takes 5–7 business days. "
        "Express shipping (2 days) is available for an additional fee."
    ),
    "warranty": (
        "Warranty: all hardware products include a 12-month manufacturer warranty "
        "covering defects; accidental damage is not covered."
    ),
    "support": (
        "Support hours: Monday–Friday 9am–6pm IST. "
        "Email support@example.com or use the in-app chat."
    ),
}


def web_search(query: str, max_snippets: int = 3) -> str:
    """
    Fake search — match query words against MOCK_RESULTS keys.

    Real portfolios use SerpAPI; we avoid cost with hardcoded snippets.
    """
    q = query.lower()
    hits: list[str] = []
    for keyword, snippet in MOCK_RESULTS.items():
        if keyword in q:
            hits.append(f"[{keyword}] {snippet}")

    if not hits:
        # Fallback: return first N snippets so the agent always gets something
        hits = [f"[{k}] {v}" for k, v in list(MOCK_RESULTS.items())[:max_snippets]]
        return "No exact keyword match. Related snippets:\n" + "\n".join(hits)

    return "\n".join(hits[:max_snippets])


if __name__ == "__main__":
    print(web_search("What is the refund policy?"))
