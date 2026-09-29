"""Workflow benchmark grading — keywords, numbers, required tools."""

from __future__ import annotations

import re
from typing import Any


def _numbers_in_text(text: str) -> list[float]:
    out: list[float] = []
    for m in re.finditer(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d+", text):
        raw = m.group(0).replace(",", "")
        try:
            out.append(float(raw))
        except ValueError:
            continue
    return out


def keyword_pass(text: str, expected: list[str]) -> bool:
    if not expected:
        return True
    lower = text.lower()
    hits = sum(1 for kw in expected if kw.lower() in lower)
    return hits >= max(1, (len(expected) + 1) // 2)


def numeric_pass(text: str, target: float, tolerance: float = 0.02) -> bool:
    if target == 0:
        return any(abs(n) < 1e-6 for n in _numbers_in_text(text))
    for n in _numbers_in_text(text):
        if abs(n - target) / abs(target) <= tolerance:
            return True
    return False


def tools_pass(required: list[str], used: list[str]) -> bool:
    if not required:
        return True
    used_set = set(used)
    return all(r in used_set for r in required)


def grade_task(
    task: dict[str, Any],
    answer: str,
    tools_used: list[str],
    tool_results: list[str] | None = None,
) -> dict[str, bool]:
    keywords = task.get("expected_contains", [])
    has_numeric = task.get("expected_numeric") is not None
    combined_text = answer
    if tool_results:
        combined_text = answer + "\n" + "\n".join(tool_results)

    if keywords and has_numeric:
        # Accept keyword OR numeric in answer or calculator tool output
        tol = float(task.get("numeric_tolerance", 0.02))
        target = float(task["expected_numeric"])
        content_ok = (
            keyword_pass(answer, keywords)
            or numeric_pass(answer, target, tol)
            or numeric_pass(combined_text, target, tol)
        )
    elif has_numeric:
        content_ok = numeric_pass(
            answer, float(task["expected_numeric"]), float(task.get("numeric_tolerance", 0.02))
        )
    else:
        content_ok = keyword_pass(answer, keywords)
    tools_ok = tools_pass(task.get("required_tools", []), tools_used)
    return {
        "content": content_ok,
        "tools": tools_ok,
        "pass": content_ok and tools_ok,
    }
