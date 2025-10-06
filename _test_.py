import os
import sys
import smtplib
import json
import csv
from dotenv import load_dotenv

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from company_finder import setup_gemini, find_companies_with_emails, save_companies_to_csv
from main import load_recipients_from_csv, send_emails, build_email_content

def test_smtp_connection():
    """Test SMTP server connection."""
    print("\n🔍 Testing SMTP connection...")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            print("✅ SMTP connection successful!")
            return True
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        return False

def test_gemini_connection():
    """Test Gemini API connection."""
    print("\n🤖 Testing Gemini API connection...")
    try:
        model = setup_gemini(os.getenv("GEMINI_API_KEY"))
        # Simple test query
        response = model.generate_content("Say 'Hello, World!'")
        print("✅ Gemini API connection successful!")
        return True
    except Exception as e:
        print(f"❌ Gemini API connection failed: {e}")
        return False

def test_company_search():
    """Test company search functionality."""
    print("\n🔎 Testing company search...")
    test_csv = "test_recipients.csv"
    
    try:
        model = setup_gemini(os.getenv("GEMINI_API_KEY"))
        test_query = "AI companies in New York"
        max_results = 2  # Keep it small for testing
        
        print(f"Searching for: {test_query}")
        companies = find_companies_with_emails(test_query, model, max_results)
        
        if not companies or len(companies) == 0:
            print("❌ No companies found")
            return False
            
        print(f"✅ Found {len(companies)} companies:")
        for i, company in enumerate(companies[:3], 1):  # Show first 3 for brevity
            print(f"   {i}. {company.get('name', 'N/A')} - {company.get('email', 'N/A')}")
        
        # Test saving to CSV
        save_companies_to_csv(companies, test_csv)
        print(f"✅ Saved companies to {test_csv}")
        
        # Verify CSV was created and has data
        with open(test_csv, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            print(f"✅ Verified {len(rows)} rows in {test_csv}")
            
            # Verify the name field uses company name
            for row in rows:
                if row['name'] != row['company_name']:
                    print(f"❌ Name field should match company_name")
                    return False
            print("✅ Verified name field matches company_name")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: {test_csv} not found")
        return False
    except Exception as e:
        print(f"❌ Error in test_company_search: {str(e)}")
        return False

def test_email_sending():
    """Test email sending functionality."""
    print("\n📧 Testing email sending...")
    try:
        test_recipient = {
            'name': 'Test Company',
            'email': os.getenv("EMAIL_ADDRESS"),  # Send to yourself for testing
            'company_name': 'Test Company Inc.'
        }
        
        # Build test email
        subject, body = build_email_content(test_recipient)
        print(f"Subject: {subject}")
        print(f"Body preview: {body[:100]}...")
        
        # Test sending (will actually send an email)
        print("Sending test email...")
        send_emails([test_recipient])
        print("✅ Test email sent successfully! Check your inbox.")
        return True
        
    except Exception as e:
        print(f"❌ Error in test_email_sending: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("🚀 Starting Email Sender Test Suite...")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Run tests
    tests = [
        ("SMTP Connection", test_smtp_connection),
        ("Gemini API Connection", test_gemini_connection),
        ("Company Search", test_company_search),
        ("Email Sending", test_email_sending)
    ]
    
    results = {}
    for name, test_func in tests:
        print(f"\n🔵 Running test: {name}")
        print("-" * 30)
        results[name] = test_func()
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print("=" * 50)
    for name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {name}")
    
    # Final status
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All tests passed successfully!")
    else:
        print("\n⚠️  Some tests failed. Please check the logs above.")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()
