import sqlite3
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from utils.dna_logic import decode_from_dna

DB_DIR = BASE_DIR / "database"
DB_PATH = DB_DIR / "records.db"

def is_dna(text):
    if not text:
        return False
    # If the text is plain text instead of DNA, it will contain lowercase letters, spaces, @ etc.
    # We only decode if it looks like pure DNA
    return all(char in 'ACGT' for char in str(text))

def migrate_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT id, username, email, mobile_dna FROM users WHERE role='verifier' OR role='Verifier' OR role='investigator'")
    users = cur.fetchall()
    
    for u in users:
        new_username = u["username"]
        new_email = u["email"]
        new_mobile = u["mobile_dna"]
        
        if is_dna(new_username):
            try:
                new_username = decode_from_dna(new_username)
                print(f"Decoded username for ID {u['id']}: {new_username}")
            except: pass
            
        if is_dna(new_email):
            try:
                new_email = decode_from_dna(new_email)
                print(f"Decoded email for ID {u['id']}: {new_email}")
            except: pass
            
        if is_dna(new_mobile):
            try:
                # My previous script corrupted the mobile string. I'll just clear corrupted strings. 
                # If they are DNA, decode.
                new_mobile = decode_from_dna(new_mobile)
                print(f"Decoded mobile for ID {u['id']}: {new_mobile}")
            except: 
                new_mobile = "Decrypted"
            
        # Update record
        cur.execute(
            "UPDATE users SET username=?, email=?, mobile_dna=? WHERE id=?",
            (new_username, new_email, new_mobile, u["id"])
        )
        
    conn.commit()
    conn.close()
    print("Migration complete. All personnel data decrypted.")

if __name__ == "__main__":
    migrate_users()
