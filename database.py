#database
import sqlite3

DATABASE_NAME = "support_tickets.db"


def connect_db():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            priority TEXT DEFAULT 'Normal',
            category TEXT DEFAULT 'Uncategorized',
            sentiment TEXT DEFAULT 'Unknown',
            ai_suggested_response TEXT DEFAULT ''
        )
    """)

    # Add new columns to an older database if needed
    existing_columns = {
        row["name"]
        for row in cursor.execute(
            "PRAGMA table_info(tickets)"
        ).fetchall()
    }

    new_columns = {
        "category": "TEXT DEFAULT 'Uncategorized'",
        "sentiment": "TEXT DEFAULT 'Unknown'",
        "ai_suggested_response": "TEXT DEFAULT ''"
    }

    for column, definition in new_columns.items():
        if column not in existing_columns:
            cursor.execute(
                f"ALTER TABLE tickets ADD COLUMN {column} {definition}"
            )

    connection.commit()
    connection.close()
