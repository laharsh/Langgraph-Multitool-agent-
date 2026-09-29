"""
sql_tool.py — read-only SQL against the demo company database.

Safety: only SELECT statements are allowed (no INSERT/UPDATE/DELETE).
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

from src.config import DB_PATH

_FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|ATTACH|PRAGMA|VACUUM)\b",
    re.IGNORECASE,
)


def sql_query(query: str, db_path: Path | None = None) -> str:
    """
    Run a read-only SQL query and return rows as plain text.

    Args:
        query: SQL SELECT statement.
        db_path: Override DB path (for tests).

    Returns:
        Column headers + rows, or an error message string.
    """
    q = query.strip().rstrip(";")
    if not q.upper().startswith("SELECT"):
        return "Error: only SELECT queries are allowed."
    if _FORBIDDEN.search(q):
        return "Error: write/DDL statements are not allowed."

    path = db_path or DB_PATH
    if not path.exists():
        return f"Error: database not found at {path}. Run: python scripts/seed_db.py"

    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        cur = conn.execute(q)
        rows = cur.fetchall()
        conn.close()
    except sqlite3.Error as exc:
        return f"SQL error: {exc}"

    if not rows:
        return "(no rows)"

    cols = rows[0].keys()
    lines = [" | ".join(cols)]
    lines.append("-" * len(lines[0]))
    for row in rows:
        lines.append(" | ".join(str(row[c]) for c in cols))
    return "\n".join(lines)


if __name__ == "__main__":
    print(sql_query("SELECT quarter, product, SUM(revenue) AS total FROM sales GROUP BY quarter, product LIMIT 5"))
