import sqlite3
import os
from pathlib import Path

# Paths
BASE_DIR = Path("d:/final year project/crime") # Explicit absolute path to the project root
DB_PATH = BASE_DIR / "database" / "records.db"

def check_users():
    if not DB_PATH.exists():
        print(f"Error: Database file not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("SELECT id, role, username, email FROM users")
        users = cur.fetchall()
        
        print(f"\n--- USER LIST ({len(users)} found) ---")
        for u in users:
            print(f"ID: {u['id']} | Role: {u['role']} | Name (DNA): {u['username']} | Email (DNA): {u['email']}")
        
        print("\n--- DATABASE CHECK COMPLETE ---")
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")

if __name__ == "__main__":
    check_users()
