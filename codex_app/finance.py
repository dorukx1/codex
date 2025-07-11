import sqlite3
from typing import List, Tuple
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, date TEXT, category TEXT, amount REAL)"
    )
    conn.commit()
    conn.close()


def add_expense(category: str, amount: float, date: str = None) -> None:
    date = date or datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",
        (date, category, amount),
    )
    conn.commit()
    conn.close()


def get_monthly_summary(month: str) -> List[Tuple[str, float]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = ? GROUP BY category",
        (month,),
    )
    rows = c.fetchall()
    conn.close()
    return rows
