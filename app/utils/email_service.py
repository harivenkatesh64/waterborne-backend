import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(to_email, subject, message):

    # If a single email is passed, convert it to a list
    if isinstance(to_email, str):
        to_email = [to_email]

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = ", ".join(to_email)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)

        # send email to all recipients
        server.sendmail(SMTP_EMAIL, to_email, msg.as_string())

        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print("Email sending failed:", str(e))