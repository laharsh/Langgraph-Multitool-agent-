"""
agent_graph.py — LangGraph state machine (agent ↔ tools loop).

Nodes:
  - agent: LLM decides to call tools or answer
  - tools: run selected tools, append results to messages
"""

from __future__ import annotations

from typing import Annotated, Any, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from src.config import MAX_AGENT_LOOPS
from src.llm import get_chat_model
from src.tools.langchain_tools import AGENT_TOOLS

SYSTEM_PROMPT = """You are an AI governance operations assistant (GRC + regulatory Q&A).

SQLite tables:
- ai_systems(name, risk_tier, primary_framework, owner_department)
- compliance_findings(framework, quarter, severity, status, summary)
- sales(quarter, product, revenue, units) — demo ops data
- employees, support_tickets

Tools:
- sql_query: internal register & findings (SELECT only)
- calculator: math on SQL results or user numbers
- web_search: short internal policy snippets (refund/shipping)
- knowledge_search: EU AI Act, NIST AI RMF, India DPDP via regulatory RAG API

Rules:
1. Never invent regulation text or counts — use tools first.
2. SQL: use COUNT/SUM aggregates, not long row dumps.
3. Any NIST / EU / DPDP / legal question → MUST call knowledge_search.
4. Combine tool outputs into one concise answer for the user.
5. On tool Error (e.g. RAG API down), say so clearly.
"""


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[dict[str, Any]]


def _build_graph():
    llm = get_chat_model().bind_tools(AGENT_TOOLS)
    tool_node = ToolNode(AGENT_TOOLS)

    def agent_node(state: AgentState) -> dict:
        response = llm.invoke(state["messages"])
        return {"messages": [response]}

    def tools_node(state: AgentState) -> dict:
        """Run tools and append a structured log entry per call."""
        last = state["messages"][-1]
        log = list(state.get("tool_calls", []))
        pending: list[dict[str, Any]] = []
        if isinstance(last, AIMessage) and last.tool_calls:
            for tc in last.tool_calls:
                entry = {"tool": tc["name"], "args": tc.get("args", {})}
                log.append(entry)
                pending.append(entry)

        tool_result = tool_node.invoke(state)
        messages = tool_result["messages"]
        tool_msgs = [m for m in messages if m.type == "tool"]
        for entry, tmsg in zip(pending, tool_msgs):
            entry["result"] = (tmsg.content or "")[:800]

        return {"messages": messages, "tool_calls": log}

    def route_after_agent(state: AgentState) -> str:
        last = state["messages"][-1]
        if isinstance(last, AIMessage) and last.tool_calls:
            return "tools"
        return END

    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", route_after_agent, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")
    return graph.compile()


_compiled_graph = None


def get_agent_graph():
    """Lazy compile so imports/tests do not require a running LLM."""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = _build_graph()
    return _compiled_graph


def _final_text(messages: list[BaseMessage]) -> str:
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content and not msg.tool_calls:
            text = msg.content
            if isinstance(text, str):
                return text.strip()
            return str(text).strip()
    if messages:
        last = messages[-1]
        return str(getattr(last, "content", last))
    return ""


def run_agent(question: str) -> dict[str, Any]:
    """
    Run the LangGraph agent on a user question.

    Returns:
        answer: final assistant text
        tool_calls: list of {tool, args, result?}
        messages: full message list (for debugging)
    """
    initial: AgentState = {
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=question),
        ],
        "tool_calls": [],
    }
    # Each agent↔tools cycle is 2 steps; cap loops via recursion_limit
    config = {"recursion_limit": max(4, MAX_AGENT_LOOPS * 2 + 2)}
    final_state = get_agent_graph().invoke(initial, config=config)
    return {
        "question": question,
        "answer": _final_text(final_state["messages"]),
        "tool_calls": final_state.get("tool_calls", []),
        "messages": final_state["messages"],
    }
