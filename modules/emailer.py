# modules/emailer.py
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EXECUTIVE_ORDERS_EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EXECUTIVE_ORDERS_EMAIL_PASSWORD")

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
    msg["To"] = "someone@domain.com"
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

