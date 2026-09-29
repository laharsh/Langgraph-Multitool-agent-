"""
calculator_tool.py — safe math for the agent (no eval of arbitrary Python).
"""

from __future__ import annotations

import ast
import operator
from typing import Any

# Allowed binary ops only — keeps expressions simple and safe.
_OPS: dict[type, Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    raise ValueError("unsupported expression")


def calculator(expression: str) -> str:
    """
    Evaluate a math expression like '45000 * 0.18'.

    Only numbers and + - * / ** ( ) are allowed.
    """
    expr = expression.strip()
    if not expr:
        return "Error: empty expression"
    try:
        tree = ast.parse(expr, mode="eval")
        value = _eval_node(tree.body)
        # Pretty int when exact
        if value == int(value):
            return str(int(value))
        return str(round(value, 6))
    except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as exc:
        return f"Error: {exc}"


if __name__ == "__main__":
    print(calculator("45000 * 0.18"))
