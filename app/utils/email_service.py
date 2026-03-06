import os
import requests
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_email(to_email, subject, message):

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "onboarding@resend.dev",
                "to": ["harivenkatesh463@gmail.com"],   # always send to your email
                "subject": subject,
                "html": message
            }
        )

        print("Email status:", response.status_code)
        print("Response:", response.text)

    except Exception as e:
        print("Email sending failed:", str(e))