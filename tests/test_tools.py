"""Phase 1 — each tool works in isolation."""

from pathlib import Path

import pytest

from src.tools.calculator_tool import calculator
from src.tools.search_tool import web_search
from src.tools.sql_tool import sql_query


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """Minimal sales table for SQL tests."""
    import sqlite3

    path = tmp_path / "test.db"
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE sales (id INT, quarter TEXT, product TEXT, revenue REAL, units INT)"
    )
    conn.execute(
        "INSERT INTO sales VALUES (1, 'Q3', 'Alpha', 45000.0, 120)"
    )
    conn.commit()
    conn.close()
    return path


def test_calculator_basic():
    assert calculator("15 * 1.08") == "16.2"
    assert calculator("45000 * 0.18") == "8100"


def test_calculator_rejects_bad_input():
    assert calculator("__import__('os')").startswith("Error:")


def test_sql_select(db_path: Path):
    out = sql_query(
        "SELECT product, revenue FROM sales WHERE quarter='Q3' AND product='Alpha'",
        db_path=db_path,
    )
    assert "Alpha" in out
    assert "45000" in out


def test_sql_blocks_delete(db_path: Path):
    assert "Error" in sql_query("DELETE FROM sales", db_path=db_path)


def test_web_search_refund():
    out = web_search("refund policy")
    assert "30 days" in out.lower()


def test_web_search_fallback():
    out = web_search("quantum computing")
    assert "snippet" in out.lower() or "shipping" in out.lower()
