import os
import requests
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


def send_email(to_email, subject, message):

    # allow single email or list of emails
    if isinstance(to_email, str):
        to_email = [to_email]

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "onboarding@resend.dev",
                "to": to_email,
                "subject": subject,
                "html": message
            }
        )

        print("Email sent:", response.status_code)

    except Exception as e:
        print("Email sending failed:", str(e))