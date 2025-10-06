import google.generativeai as genai
import os
import json
import time
from typing import List, Dict
import csv

def setup_gemini(api_key: str):
    """Initialize the Gemini API with the provided API key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-pro')

def find_companies_with_emails(query: str, model, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Search for companies and their contact emails based on a search query.
    """
    prompt = f"""Find {max_results} companies that match this search query: "{query}".
    For each company, provide:
    1. Company name
    2. Website URL
    3. Contact email (preferably a general contact or info email)
    4. Industry
    5. Brief description
    
    Format the response as a JSON list of objects with these exact keys:
    - name (string)
    - website (string)
    - email (string)
    - industry (string)
    - description (string)
    """
    
    try:
        response = model.generate_content(prompt)
        # Extract JSON from the response
        json_str = response.text[response.text.find('['):response.text.rfind(']')+1]
        companies = json.loads(json_str)
        return companies[:max_results]
    except Exception as e:
        print(f"Error finding companies: {e}")
        return []

def save_companies_to_csv(companies: List[Dict[str, str]], filename: str = 'recipients.csv') -> bool:
    """Save the found companies to a CSV file."""
    fieldnames = ['name', 'email', 'company_name', 'website', 'industry', 'description']
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company in companies:
                writer.writerow({
                    'name': 'Hiring Manager',
                    'email': company.get('email', ''),
                    'company_name': company.get('name', ''),
                    'website': company.get('website', ''),
                    'industry': company.get('industry', ''),
                    'description': company.get('description', '')
                })
        print(f"Successfully saved {len(companies)} companies to {filename}")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False

def find_and_save_companies(search_query: str, max_results: int = 10) -> bool:
    """Main function to find companies and save them to CSV."""
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return False
    
    try:
        model = setup_gemini(gemini_api_key)
        print(f"Searching for {search_query}...")
        companies = find_companies_with_emails(search_query, model, max_results)
        
        if companies:
            if save_companies_to_csv(companies):
                print("\nCompanies have been saved to recipients.csv")
                return True
        else:
            print("No companies found or there was an error.")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
