import smtplib
import ssl
from email.message import EmailMessage
import csv
from typing import List, Dict
import os
from dotenv import load_dotenv
from template import SUBJECT_TEMPLATE, EMAIL_BODY, render_subject, render_body

# Load environment variables from .env file
load_dotenv()

# --- IMPORTANT CONFIGURATION NOTES ---
# 1. Use an "App Password":
#    If you are using Gmail, Outlook, or another major email provider,
#    you MUST use an "App Password" (not your main account password) for security.
#    Search online for "How to generate an App Password for [Your Email Provider]".
#
# 2. Server/Port:
#    - Gmail: SMTP_SERVER = "smtp.gmail.com", SMTP_PORT = 587 (TLS)
#    - Outlook/Office 365: SMTP_SERVER = "smtp.office365.com", SMTP_PORT = 587 (TLS)
#    - Yahoo: SMTP_SERVER = "smtp.mail.yahoo.com", SMTP_PORT = 587 (TLS)

# --- SENDER CREDENTIALS ---
SENDER_EMAIL = os.getenv('EMAIL_ADDRESS')
SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

def build_email_content(recipient: Dict[str, str]) -> tuple[str, str]:
    """Render subject and body using templates from template.py with safe defaults."""
    context = {
        "name": recipient.get("name", "there"),
        # template.py expects company_name; provide a default if missing in CSV
        "company_name": recipient.get("company_name", "your company"),
    }
    subject = render_subject(context)
    body = render_body(context)
    return subject, body


def load_recipients_from_csv(filepath: str) -> List[Dict[str, str]]:
    """Loads recipient data from a CSV file."""
    try:
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            # Read the CSV file
            reader = csv.DictReader(file)
            # Convert to list of dictionaries and add project_area field
            recipients = []
            for row in reader:
                row['project_area'] = 'General'  # Default project area
                recipients.append(row)
            return recipients
    except FileNotFoundError:
        print(f"Error: CSV file not found at {filepath}")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return []


def send_emails(recipients: List[Dict[str, str]]):
    """
    Connects to the SMTP server and sends a customized email to each recipient.
    """
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Error: Email credentials not found in environment variables.")
        return

    print(f"Attempting to connect to {SMTP_SERVER}:{SMTP_PORT}...")

    # Create a default SSL context for security
    context = ssl.create_default_context()
    emails_sent = 0
    errors = 0

    try:
        # Use a context manager to ensure the connection is closed
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            # Start Transport Layer Security (TLS) encryption
            server.starttls(context=context)
            # Login to the server
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Successfully logged into the SMTP server.")

            for recipient in recipients:
                try:
                    # 1. Prepare the email message object
                    msg = EmailMessage()
                    
                    # Render subject and body via template helpers
                    subject, body = build_email_content(recipient)

                    msg['Subject'] = subject
                    msg['From'] = SENDER_EMAIL
                    msg['To'] = recipient['email']
                    msg.set_content(body)

                    # 2. Send the email
                    server.send_message(msg)
                    print(f"Email sent to {recipient['name']} ({recipient['email']})")
                    emails_sent += 1

                except Exception as e:
                    errors += 1
                    print(f"Error sending to {recipient.get('email', 'unknown')}: {str(e)}")
                    continue

    except Exception as e:
        print(f"Error: {str(e)}")
        return

    print(f"\nEmail sending complete!")
    print(f"Successfully sent: {emails_sent}")
    print(f"Failed to send: {errors}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Load recipients from CSV
    recipients = load_recipients_from_csv('recipients.csv')
    
    if not recipients:
        print("No recipients found or error loading recipients. Exiting.")
    else:
        print(f"Loaded {len(recipients)} recipients from CSV.")
        send_emails(recipients)