import os
import sqlite3
from datetime import datetime, timezone

# Absolute path to the database
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "eo_watch.db"))

def trigger_alert(tag="TEST"):
    """Insert a dummy alert entry into the executive_orders table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    dummy_title = f"[DUMMY] Alert Triggered ({tag})"
    dummy_date = datetime.now(timezone.utc).isoformat()
    dummy_url = f"https://example.com/triggered/{tag}"

    cursor.execute("""
        INSERT INTO executive_orders (title, date, url)
        VALUES (?, ?, ?)
    """, (dummy_title, dummy_date, dummy_url))
   
    new_id = cursor.lastrowid # get auto increment ID of inserted row
    
    cursor.execute("""
        SELECT * FROM executive_orders WHERE id = ?
        """, (new_id,))
    row = cursor.fetchone()
    print(f"Inserted row: {row}")

    conn.commit()
    conn.close()
    print(f"🧨 Dummy alert triggered: {tag}")


def clear_alert(tag="TEST"):
    """Remove dummy alert entries with the given tag."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    pattern = f"%[DUMMY]%{tag}%"
    cursor.execute("""
        DELETE FROM executive_orders
        WHERE title LIKE ?
    """, (pattern,))
    
    conn.commit()
    conn.close()
    print(f"✅ Dummy alert cleared: {tag}")

