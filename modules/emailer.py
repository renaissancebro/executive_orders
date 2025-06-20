# modules/emailer.py
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from pathlib import Path

# Get the path to the parent directory (where your main script and .env live)
project_root = Path(__file__).resolve().parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

print("📍 Loading .env from:", env_path)


EMAIL_ADDRESS = os.getenv("EXECUTIVE_ORDERS_EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EXECUTIVE_ORDERS_EMAIL_PASSWORD")
RECIPIENTS = [email.strip() for email in os.getenv("EXECUTIVE_ORDERS_EMAIL_RECIPIENTS", "").split(",") if email.strip()]

print("📧 Email:", EMAIL_ADDRESS)
print("🔑 Password present:", EMAIL_PASSWORD is not None)


def make_email(meta):
    subject = f"📢 New Executive Order: “{meta['title']}”"
    body = (
        f"📝 Title: {meta['title']}\n"
        f"📅 Date: {meta['date']}\n"
        f"🔗 Link: {meta['url']}\n\n"
        f"Auto-sent by EO Watchdog — your policy radar.\n"
    )
    return subject, body

import smtplib
from email.message import EmailMessage

def send_mail(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = ", ".join(RECIPIENTS)
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent!")
    except smtplib.SMTPAuthenticationError as e:
        print("❌ Authentication failed. Check email/password.")
        print(e.smtp_error.decode() if hasattr(e, "smtp_error") else e)
    except Exception as e:
        print("❌ Email sending error:", e)

