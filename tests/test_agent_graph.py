"""Agent wiring tests (no live LLM required)."""

from langchain_core.messages import AIMessage, HumanMessage

from src.agent_graph import _final_text
from src.tools.langchain_tools import AGENT_TOOLS


def test_agent_has_four_tools():
    names = {t.name for t in AGENT_TOOLS}
    assert names == {"sql_query", "calculator", "web_search", "knowledge_search"}


def test_final_text_picks_last_ai_message():
    messages = [
        HumanMessage(content="hi"),
        AIMessage(content="The total is 8100."),
    ]
    assert _final_text(messages) == "The total is 8100."
