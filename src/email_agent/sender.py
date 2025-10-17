# src/email_agent/sender.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.security.security import mail_id, mail_pass

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
USERNAME = mail_id
PASSWORD = mail_pass


def send_email(to_address: str, subject: str, body: str):
    """
    Send an email using Gmail SMTP.
    """
    msg = MIMEMultipart()
    msg["From"] = USERNAME
    msg["To"] = to_address
    msg["Subject"] = subject

    # Attach plain text body
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, to_address, msg.as_string())
        print(f"✅ Email sent to {to_address}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
