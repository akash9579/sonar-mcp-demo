# Repository layer — all database access for the users table goes through here.
# CLAUDE.md requires new code to route DB access through this module instead of
# writing raw SQL directly in route handlers (see main.py).

import os
import sqlite3
from typing import Any

DATABASE_URL_ENV_VAR = "DATABASE_URL"


def get_database_url() -> str:
    """
    Return the configured database connection string.

    Read from the DATABASE_URL environment variable rather than a literal in
    source, so credentials never live in a tracked file. Populate it locally
    from app-credentials.txt (gitignored) via `export $(cat app-credentials.txt | xargs)`
    or an equivalent env loader, and from a secrets manager in deployed environments.
    """
    url = os.environ.get(DATABASE_URL_ENV_VAR)
    if not url:
        raise RuntimeError(
            f"{DATABASE_URL_ENV_VAR} is not set. Set it in the environment "
            "(see app-credentials.txt locally) rather than hardcoding it."
        )
    return url


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


def find_users_by_name_substring(name_substring: str) -> list[dict[str, Any]]:
    """
    Look up users whose name contains the given substring, using a
    parameterized LIKE query.

    LIKE wildcard characters in the input (% and _) are escaped so the
    substring is matched literally rather than as a pattern.
    """
    escaped = (
        name_substring.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    )
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE name LIKE ? ESCAPE '\\'",
            (f"%{escaped}%",),
        )
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


def get_user_by_email(email: str) -> dict[str, Any] | None:
    """Look up a single user by email using a parameterized query."""
    conn = _get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()