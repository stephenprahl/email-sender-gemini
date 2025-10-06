import smtplib
import ssl
from email.message import EmailMessage
import csv
from typing import List, Dict
import os
import argparse
import time
from dotenv import load_dotenv
from template import SUBJECT_TEMPLATE, EMAIL_BODY, render_subject, render_body

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
SENDER_EMAIL = os.getenv('EMAIL_ADDRESS')
SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def build_email_content(recipient: Dict[str, str]) -> tuple[str, str]:
    """Render subject and body using templates from template.py with safe defaults."""
    context = {
        "name": recipient.get("name", "there"),
        "company_name": recipient.get("company_name", "your company"),
    }
    subject = render_subject(context)
    body = render_body(context)
    return subject, body

def load_recipients_from_csv(filepath: str) -> List[Dict[str, str]]:
    """Loads recipient data from a CSV file."""
    try:
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)  # Convert to list to read all rows
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def send_emails(recipients: List[Dict[str, str]]):
    """Send emails to the list of recipients."""
    if not recipients:
        print("No recipients to email.")
        return

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print(f"Successfully connected to {SMTP_SERVER}")

            # Send emails
            for i, recipient in enumerate(recipients, 1):
                if not recipient.get('email'):
                    print(f"Skipping recipient {i}: No email address provided")
                    continue

                try:
                    subject, body = build_email_content(recipient)
                    
                    # Create message
                    msg = EmailMessage()
                    msg['From'] = SENDER_EMAIL
                    msg['To'] = recipient['email']
                    msg['Subject'] = subject
                    msg.set_content(body)

                    # Send email
                    server.send_message(msg)
                    print(f"Sent email {i}/{len(recipients)} to {recipient['email']}")

                    # Be nice to the email server
                    if i < len(recipients):
                        time.sleep(2)  # 2 second delay between emails

                except Exception as e:
                    print(f"Error sending to {recipient.get('email', 'unknown')}: {e}")

    except Exception as e:
        print(f"Error connecting to email server: {e}")
        return

def main():
    parser = argparse.ArgumentParser(description='Send personalized emails to companies.')
    parser.add_argument('--search', type=str, help='Search query to find companies (e.g., "AI companies in New York")')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum number of companies to find')
    parser.add_argument('--send', action='store_true', help='Send emails to the recipients')
    args = parser.parse_args()

    if args.search:
        from company_finder import find_and_save_companies
        print("Searching for companies...")
        if find_and_save_companies(args.search, args.max_results):
            print("Company search completed successfully!")
        else:
            print("Failed to find companies. Please check your API key and try again.")
            return

    if args.send:
        recipients = load_recipients_from_csv('recipients.csv')
        if not recipients:
            print("No recipients found in recipients.csv")
            return

        print(f"\nFound {len(recipients)} recipients in recipients.csv")
        confirm = input("Are you sure you want to send emails to these recipients? (y/n): ").lower()
        if confirm == 'y':
            send_emails(recipients)
        else:
            print("Email sending cancelled.")
    else:
        print("No action specified. Use --search to find companies or --send to send emails.")

if __name__ == "__main__":
    main()