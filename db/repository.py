# Repository layer — all database access for the users table goes through here.
# CLAUDE.md requires new code to route DB access through this module instead of
# writing raw SQL directly in route handlers (see main.py).

import sqlite3
from typing import Any


def _get_connection() -> sqlite3.Connection:
    """Open a connection to the local SQLite database."""
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def find_users_by_name(name: str) -> list[dict[str, Any]]:
    """
    Look up users by name using a parameterized query.

    This is the safe counterpart to database.py's execute_query() — same
    intent (search users by name), but uses a placeholder instead of raw
    string interpolation, so user input can never change the query structure.
    """
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> dict[str, Any] | None:
    """Look up a single user by id using a parameterized query."""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()