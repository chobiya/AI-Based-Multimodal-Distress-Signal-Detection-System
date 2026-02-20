import sqlite3

DB_NAME = "alertify.db"

# Initialize DB with users table if not exists
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password BLOB,
            first_name TEXT,
            last_name TEXT
        )
    """)
    conn.commit()
    conn.close()

# Create new user
def create_user(username, password, first_name, last_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, first_name, last_name) VALUES (?, ?, ?, ?)",
            (username, password, first_name, last_name)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # username already exists
    finally:
        conn.close()
    return True

# Authenticate user by username
def authenticate_user(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, first_name, last_name FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "username": row[0],
            "password": row[1],  # hashed password
            "first_name": row[2],
            "last_name": row[3]
        }
    return None
