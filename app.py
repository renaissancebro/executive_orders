from flask import Flask, jsonify
from modules.check import check_last_policy
from modules.scraper import grab_meta_data
from modules.emailer import make_email, send_mail

app = Flask(__name__)

@app.route("/")
def health_check():
    return "🟢 EO Watchdog is live."

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

@app.route("/latest")
def latest():
    import sqlite3
    conn = sqlite3.connect("outputs/output/my_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, date, url FROM scraped_data ORDER BY id DESC LIMIT 1")
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
    app.run(debug=True)
