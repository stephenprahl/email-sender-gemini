# 📧 Email Sender Application

A Python-based email automation tool that sends personalized emails to multiple recipients using data from a CSV file. This application is designed to help businesses and individuals send customized, bulk emails with personalized content.

## ✨ Features

- **Bulk Email Sending**: Send personalized emails to multiple recipients at once
- **Template-Based**: Customize email subjects and bodies using templates
- **CSV Integration**: Load recipient data from a CSV file
- **Secure Authentication**: Uses environment variables to store sensitive information
- **SMTP Support**: Compatible with major email providers (Gmail, Outlook, etc.)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- An email account with SMTP access

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd email-sender
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. Create a `.env` file in the project root with your email credentials:
   ```
   EMAIL_ADDRESS=your.email@example.com
   EMAIL_PASSWORD=your_app_password
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   ```

   > **Note**: For Gmail, you'll need to use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

2. Update the `recipients.csv` file with your recipient list:
   ```csv
   name,email,company_name
   John Doe,john@example.com,Acme Inc.
   Jane Smith,jane@example.com,XYZ Corp
   ```

3. Customize the email templates in `template.py` to match your needs.

## 🚀 Usage

1. Update the email content in `template.py`
2. Add your recipients to `recipients.csv`
3. Run the script:
   ```bash
   python main.py
   ```

## 📝 Templates

Edit `template.py` to customize:
- `SUBJECT_TEMPLATE`: The subject line of your emails
- `EMAIL_BODY`: The main content of your emails

Use placeholders like `{name}` and `{company_name}` which will be replaced with actual values from your CSV file.

## 🔒 Security

- Never commit your `.env` file or sensitive information to version control
- Use environment variables for all sensitive data
- Consider using a dedicated email service for production use

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

Built with ❤️ by [Your Name]
