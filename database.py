import sqlite3
from typing import Any


_DATABASE_PATH = "users.db"
_SELECT_USER_BY_NAME = "SELECT * FROM users WHERE name = (?)"


def execute_query(raw_query: str) -> list[tuple[Any, ...]]:
    if not isinstance(raw_query, str):
        raise TypeError("raw_query must be a string")

    with sqlite3.connect(_DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(_SELECT_USER_BY_NAME, (raw_query,))
        return cursor.fetchall()