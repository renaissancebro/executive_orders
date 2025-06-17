# modules/check.py
import sqlite3
from modules.scraper import fetch_latest
import os
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "eo_watch.db"))


def check_last_policy():
    latest = fetch_latest()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS executive_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        url TEXT
    )
""")

    cursor.execute("SELECT title FROM executive_orders ORDER BY ROWID DESC LIMIT 1")
    row = cursor.fetchone()
    print("Fetched latest:", latest)
    print("Existing row:", row)

    # Only insert if it’s actually new
    if not row or row[0] != latest["title"]:
        cursor.execute("INSERT INTO executive_orders (title, date, url) VALUES (?, ?, ?)",
                       (latest["title"], latest["date"], latest["url"]))
        print("Inserted row ID:", cursor.lastrowid)
        conn.commit()
        conn.close()
        return True  # ✅ New policy detected and saved
    else:
        conn.close()
        return False  # ❌ No change, don’t re-save
