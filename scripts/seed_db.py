"""
seed_db.py — generate demo SQLite data for the SQL tool.

Tables: sales, employees, support_tickets, ai_systems, compliance_findings (governance ops demo).
"""

from __future__ import annotations

import random
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Allow `python scripts/seed_db.py` from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from faker import Faker

from src.config import DB_PATH, ensure_dirs

fake = Faker()
Faker.seed(42)
random.seed(42)

PRODUCTS = ["Alpha", "Beta", "Gamma", "Delta"]
QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
DEPARTMENTS = ["Sales", "Engineering", "Support", "Finance", "HR"]
TOPICS = ["billing", "refund", "shipping", "warranty", "login", "api"]


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS sales;
        DROP TABLE IF EXISTS employees;
        DROP TABLE IF EXISTS support_tickets;
        DROP TABLE IF EXISTS ai_systems;
        DROP TABLE IF EXISTS compliance_findings;

        CREATE TABLE sales (
            id INTEGER PRIMARY KEY,
            quarter TEXT NOT NULL,
            product TEXT NOT NULL,
            revenue REAL NOT NULL,
            units INTEGER NOT NULL
        );

        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            hire_date TEXT NOT NULL
        );

        CREATE TABLE support_tickets (
            id INTEGER PRIMARY KEY,
            topic TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE ai_systems (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            risk_tier TEXT NOT NULL,
            primary_framework TEXT NOT NULL,
            owner_department TEXT NOT NULL
        );

        CREATE TABLE compliance_findings (
            id INTEGER PRIMARY KEY,
            framework TEXT NOT NULL,
            quarter TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            summary TEXT NOT NULL
        );
        """
    )


def seed_sales(conn: sqlite3.Connection, n: int = 200) -> None:
    rows = []
    for i in range(1, n + 1):
        rows.append(
            (
                i,
                random.choice(QUARTERS),
                random.choice(PRODUCTS),
                round(random.uniform(500, 50000), 2),
                random.randint(1, 500),
            )
        )
    conn.executemany(
        "INSERT INTO sales (id, quarter, product, revenue, units) VALUES (?, ?, ?, ?, ?)",
        rows,
    )


def seed_employees(conn: sqlite3.Connection, n: int = 20) -> None:
    rows = []
    for i in range(1, n + 1):
        hire = fake.date_between(start_date="-5y", end_date="today")
        rows.append((i, fake.name(), random.choice(DEPARTMENTS), hire.isoformat()))
    conn.executemany(
        "INSERT INTO employees (id, name, department, hire_date) VALUES (?, ?, ?, ?)",
        rows,
    )


def seed_tickets(conn: sqlite3.Connection, n: int = 50) -> None:
    rows = []
    base = datetime.now() - timedelta(days=90)
    for i in range(1, n + 1):
        created = base + timedelta(days=random.randint(0, 90))
        rows.append(
            (
                i,
                random.choice(TOPICS),
                random.choice(["open", "closed", "pending"]),
                created.isoformat(timespec="seconds"),
            )
        )
    conn.executemany(
        "INSERT INTO support_tickets (id, topic, status, created_at) VALUES (?, ?, ?, ?)",
        rows,
    )


def seed_ai_systems(conn: sqlite3.Connection) -> None:
    rows = [
        (1, "Customer Support Chatbot", "high", "EU", "Engineering"),
        (2, "Fraud Scoring Model", "high", "NIST", "Risk"),
        (3, "HR Resume Screener", "high", "EU", "HR"),
        (4, "Internal Search Ranker", "limited", "NIST", "Engineering"),
        (5, "Marketing Copy Assistant", "limited", "DPDP", "Marketing"),
        (6, "Log Anomaly Detector", "minimal", "NIST", "Security"),
        (7, "Meeting Summarizer", "minimal", "DPDP", "Operations"),
    ]
    conn.executemany(
        "INSERT INTO ai_systems (id, name, risk_tier, primary_framework, owner_department) "
        "VALUES (?, ?, ?, ?, ?)",
        rows,
    )


def seed_findings(conn: sqlite3.Connection) -> None:
    rows = [
        (1, "NIST", "Q3", "high", "open", "Missing model documentation for fraud scorer"),
        (2, "NIST", "Q3", "medium", "open", "Governance policy not mapped to MAP function"),
        (3, "NIST", "Q3", "low", "closed", "Annual RMF training completed"),
        (4, "EU", "Q3", "high", "open", "High-risk system lacks conformity assessment"),
        (5, "EU", "Q2", "medium", "closed", "Data processing agreement updated"),
        (6, "DPDP", "Q3", "medium", "open", "Consent logs incomplete for marketing tool"),
        (7, "NIST", "Q2", "low", "closed", "MEASURE metrics dashboard deployed"),
        (8, "NIST", "Q3", "high", "open", "Third-party LLM vendor risk review overdue"),
    ]
    conn.executemany(
        "INSERT INTO compliance_findings (id, framework, quarter, severity, status, summary) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        rows,
    )


def main() -> None:
    ensure_dirs()
    path = Path(DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(path)
    create_schema(conn)
    seed_sales(conn)
    seed_employees(conn)
    seed_tickets(conn)
    seed_ai_systems(conn)
    seed_findings(conn)
    conn.commit()
    conn.close()

    print(f"Seeded {path}")
    print(
        "  sales: 200 | employees: 20 | tickets: 50 | "
        "ai_systems: 7 | compliance_findings: 8"
    )


if __name__ == "__main__":
    main()
