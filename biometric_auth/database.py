import sqlite3
import os

DB_PATH = "data/users.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS face_samples (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            image_path TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY,
            username TEXT,
            event TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_user(username, image_paths):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("INSERT INTO users (username) VALUES (?)", (username,))
        for path in image_paths:
            conn.execute(
                "INSERT INTO face_samples (username, image_path) VALUES (?, ?)",
                (username, path))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT username, image_path FROM face_samples").fetchall()
    conn.close()
    return rows

def get_users_list():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT username, created_at FROM users").fetchall()
    conn.close()
    return rows

def delete_user(username):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.execute("DELETE FROM face_samples WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def get_audit_logs():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT username, event, timestamp FROM audit_log ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return rows

def log_event(username, event):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO audit_log (username, event) VALUES (?, ?)",
                 (username, event))
    conn.commit()
    conn.close()