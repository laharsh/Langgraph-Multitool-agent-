"""
cli.py — terminal demo for the LangGraph agent.

Usage:
    python -m src.cli "What was Q3 revenue for product Alpha?"
    python -m src.cli   # interactive prompt
"""

from __future__ import annotations

import argparse
import json
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="LangGraph agent CLI")
    parser.add_argument("question", nargs="*", help="User question (words joined)")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print full result as JSON (includes tool_calls)",
    )
    args = parser.parse_args()

    if args.question:
        question = " ".join(args.question).strip()
    else:
        question = input("Question: ").strip()

    if not question:
        print("No question provided.", file=sys.stderr)
        raise SystemExit(1)

    from src.agent_graph import run_agent

    print(f"Question: {question}\n")
    result = run_agent(question)

    if args.json:
        # messages are not JSON-serializable by default
        out = {
            "question": result["question"],
            "answer": result["answer"],
            "tool_calls": result["tool_calls"],
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print("Answer:")
    print(result["answer"])
    if result["tool_calls"]:
        print("\nTool calls:")
        for i, tc in enumerate(result["tool_calls"], 1):
            print(f"  {i}. {tc['tool']}({tc.get('args', {})})")
            if tc.get("result"):
                preview = tc["result"].replace("\n", " ")[:120]
                print(f"     -> {preview}...")


if __name__ == "__main__":
    main()
