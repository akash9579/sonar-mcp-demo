"""
One-time setup script — creates the `users` table in users.db and seeds it
with a few sample rows so the demo endpoints (both the vulnerable one in
main.py/database.py and the repository-routed ones) have real data to query.

Run once before rehearsal:
    python seed_db.py

Safe to re-run — drops and recreates the table each time.
"""

import sqlite3

SEED_USERS = [
    ("Alice Johnson", "alice@example.com"),
    ("Bob Smith", "bob@example.com"),
    ("Carla Diaz", "carla@example.com"),
    ("David O'Brien", "david@example.com"),  # deliberate apostrophe — good for
                                              # showing why raw string
                                              # interpolation breaks/exploits
]


def main() -> None:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
        """
    )
    cursor.executemany(
        "INSERT INTO users (name, email) VALUES (?, ?)", SEED_USERS
    )

    conn.commit()
    conn.close()
    print(f"Seeded users.db with {len(SEED_USERS)} rows.")


if __name__ == "__main__":
    main()