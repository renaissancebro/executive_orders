from flask import Flask, jsonify, render_template
from modules.check import check_last_policy
from modules.scraper import grab_meta_data
from modules.emailer import make_email, send_mail
from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: check_last_policy(), trigger="interval", minutes=10)
    scheduler.start()

import os

# Absolute path for database
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "eo_watch.db"))

def init_db():
    import sqlite3
    conn = sqlite3.connect("eo_watch.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS executive_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        url TEXT
    )
    """)
    cursor.execute("SELECT COUNT(*) FROM executive_orders")
    if cursor.fetchone()[0] == 0:
        from modules.scraper import fetch_latest
        latest = fetch_latest()
        cursor.execute("INSERT INTO executive_orders (title, date, url) VALUES (?, ?, ?)",
                       (latest["title"], latest["date"], latest["url"]))
        conn.commit()
    conn.close()
init_db()

app = Flask(__name__)

@app.route("/")
def health_check():
    return "🟢 EO Watchdog is live."


@app.route("/dashboard")
def dashboard():
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title, date, url FROM executive_orders")
    alerts = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", alerts=alerts)


@app.route("/run-check")
def run_check():
    try:
        if check_last_policy():  # True = new post
            meta = grab_meta_data()
            subject, body = make_email(meta)
            send_mail(subject, body)
            return jsonify({"status": "✅ New policy found", "meta": meta})
        else:
            return jsonify({"status": "No new executive order."})
    except Exception as e:
        return jsonify({"status": "❌ Error", "details": str(e)})


@app.route("/dump-db")
def dump_db():
    import sqlite3
    conn = sqlite3.connect("eo_watch.db")
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM executive_orders ORDER BY ROWID DESC")
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify(data)


@app.route("/latest")
def latest():
    import sqlite3
    conn = sqlite3.connect("eo_watch.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, date, url FROM executive_orders ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if result:
        return jsonify({
            "title": result[0],
            "date": result[1],
            "url": result[2]
        })
    else:
        return jsonify({"status": "No records found"})


if __name__ == "__main__":
    start_scheduler(app)
    app.run(debug=True)
