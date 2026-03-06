import os
import requests
import smtplib
from email.mime.text import MIMEText

ENV = os.getenv("ENVIRONMENT")

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(to_email, subject, message):

    if ENV == "render":

        # Render → use Resend API
        requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "onboarding@resend.dev",
                "to": ["YOUR_EMAIL@gmail.com"],
                "subject": subject,
                "html": message
            }
        )

    else:

        # Localhost → use SMTP
        if isinstance(to_email, str):
            to_email = [to_email]

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SMTP_EMAIL
        msg["To"] = ", ".join(to_email)

        server = smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT))
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        server.quit()