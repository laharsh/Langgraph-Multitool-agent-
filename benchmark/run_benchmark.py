"""
Run workflow benchmark — content + required tools.

Usage:
    python benchmark/run_benchmark.py
    python benchmark/run_benchmark.py --limit 3
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from benchmark.grader import grade_task
from src.agent_service import run_chat

TASKS_PATH = Path(__file__).parent / "tasks.json"
OUTPUT_PATH = ROOT / "benchmark_results.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    tasks = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    if args.limit > 0:
        tasks = tasks[: args.limit]

    rows = []
    passed = 0
    by_workflow: dict[str, list[bool]] = {}

    for task in tasks:
        wf = task.get("workflow", "default")
        print(f"[{task['id']}] ({wf}) {task['question'][:55]}...")
        t0 = time.time()
        try:
            result = run_chat(task["question"])
            answer = result.get("answer") or ""
            tools_used = [tc["tool"] for tc in result.get("tool_calls", [])]
            tool_results = [
                str(tc.get("result") or "") for tc in result.get("tool_calls", [])
            ]
            scores = grade_task(task, answer, tools_used, tool_results)
            ok = scores["pass"]
        except Exception as exc:
            answer = ""
            tools_used = []
            scores = {"content": False, "tools": False, "pass": False}
            ok = False
            print(f"    ERROR: {exc}")
        elapsed = time.time() - t0
        if ok:
            passed += 1
        by_workflow.setdefault(wf, []).append(ok)
        rows.append(
            {
                "id": task["id"],
                "workflow": wf,
                "question": task["question"],
                "pass": ok,
                "content_ok": scores["content"],
                "tools_ok": scores["tools"],
                "tools_used": tools_used,
                "required_tools": task.get("required_tools", []),
                "seconds": round(elapsed, 2),
                "answer_preview": answer[:200],
            }
        )
        print(
            f"    pass={ok} content={scores['content']} tools={scores['tools']} "
            f"used={tools_used} ({elapsed:.1f}s)"
        )

    workflow_rates = {
        k: sum(v) / len(v) if v else 0.0 for k, v in by_workflow.items()
    }
    report = {
        "n": len(tasks),
        "pass_rate": passed / len(tasks) if tasks else 0,
        "by_workflow": workflow_rates,
        "rows": rows,
    }
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nPass rate: {report['pass_rate']:.1%} ({passed}/{len(tasks)})")
    print(f"By workflow: {workflow_rates}")
    print(f"Saved -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
