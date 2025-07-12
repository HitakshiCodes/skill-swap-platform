
import sqlite3

def init_db():
    with sqlite3.connect("skill_swap.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT,
                offer TEXT,
                want TEXT,
                availability TEXT,
                is_public INTEGER
            )
        """)


