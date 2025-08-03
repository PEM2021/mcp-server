import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  # STARTTLS port

def send_email(recipient: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = recipient

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, recipient, msg.as_string())
    except Exception as e:
        raise RuntimeError(f"❌ Failed to send email: {e}")
