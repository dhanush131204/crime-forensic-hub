import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "records.db"

def fix_corrupted_mobile():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE users SET mobile_dna='Not Provided' WHERE mobile_dna LIKE '%$%'")
    conn.commit()
    conn.close()
    print("Fixed corrupted mobile numbers.")

if __name__ == "__main__":
    fix_corrupted_mobile()
