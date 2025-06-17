🕵️‍♂️ EO Watchdog
EO Watchdog is a Flask-based dashboard and monitoring system that tracks new U.S. Executive Orders and alerts users via email when new policies are posted. It scrapes official sources and stores metadata in a local SQLite database with a web-based dashboard for review.

🔍 Features
Automatically detects and logs new Executive Orders

Sends email alerts when new EOs are found

Flask dashboard to browse latest entries

JSON endpoints for programmatic access

Modular architecture (easily extensible to other watchdogs like the Federal Register)


🚀 Live Demo
Hosted at: https://executive-orders-5luq.onrender.com
Dashboard: https://executive-orders-5luq.onrender.com/dashboard



⚙️ Setup Instructions
bash
Copy
Edit
# 1. Clone the repo
git clone https://github.com/your-username/eo-watchdog.git
cd eo-watchdog

# 2. Set up a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file with email credentials
cp .env.example .env
.env:

ini
Copy
Edit
EMAIL=you@example.com
EMAIL_PASSWORD=your_app_password
✅ API Endpoints
Route	Description
/	Health check
/run-check	Manually trigger a scan
/dashboard	View the HTML dashboard
/latest	Get latest EO as JSON
/dump-db	Dump full DB contents as JSON

🔜 Coming Soon
✅ Federal Register integration

🔄 Scheduled background monitoring

🌐 Public-facing deployment

🧪 Unit tests and test data

Maintainer
Joshua Freeman – jcfreeman23@gmail.com
