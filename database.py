import sqlite3

def init_db():
    with sqlite3.connect("skill_swap.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            profile_pic TEXT          
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skill TEXT NOT NULL,
            want TEXT,
            contact TEXT,
            location TEXT,
            mode TEXT
        )
        """)
        conn.commit()


     




