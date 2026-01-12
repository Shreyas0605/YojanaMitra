"""
Test the improved scraper on a single scheme to verify data extraction
"""

import requests
import json
import re
import sys

# Test extraction with just the MyScheme API logic
api_key = 'tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc'
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json',
    'x-api-key': api_key
}

# Get one scheme to test
print("Fetching a test scheme from MyScheme API...")
test_slug = "skill-loan-scheme"  # Using a known scheme from the database

detail_url = f"https://api.myscheme.gov.in/schemes/v6/public/schemes?slug={test_slug}&lang=en"
response = requests.get(detail_url, headers=headers, timeout=10)

if response.status_code == 200:
    data = response.json()
    
    # Save the raw JSON for inspection
    with open('test_scheme_raw.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Data fetched successfully. Saved to test_scheme_raw.json")
    print("\nAPI Response Structure:")
    print(f"- Type: {type(data)}")
    
    # Extract the 'en' content
    root = {}
    if isinstance(data, list) and data:
        root = data[0].get('en', {})
    elif isinstance(data, dict):
        if 'data' in data and isinstance(data['data'], dict):
            root = data['data'].get('en', {})
        else:
            root = data.get('en', {})
    
    if root:
        basic = root.get('basicDetails', {})
        content = root.get('schemeContent', {})
        eligibility_criteria = root.get('eligibilityCriteria', [])
        application_process = root.get('applicationProcess', [])
        
        print("\nAvailable top-level keys in 'en':")
        print(list(root.keys()))
        
        print("\nAvailable keys in 'basicDetails':")
        print(list(basic.keys()))
        
        print("\nAvailable keys in 'schemeContent':")
        print(list(content.keys()))
        
        print("\neligibilityCriteria type:", type(eligibility_criteria), "length:", len(eligibility_criteria) if isinstance(eligibility_criteria, list) else "N/A")
        print("\napplicationProcess type:", type(application_process), "length:", len(application_process) if isinstance(application_process, list) else "N/A")
        
        # Show a sample of what's in these fields
        if isinstance(eligibility_criteria, list) and len(eligibility_criteria) > 0:
            print("\nFirst eligibility item structure:")
            print(json.dumps(eligibility_criteria[0], indent=2)[:500])
        
        if 'benefits' in content:
            print("\nBenefits field type:", type(content['benefits']))
            if isinstance(content['benefits'], list) and len(content['benefits']) > 0:
                print("First benefit item:")
                print(json.dumps(content['benefits'][0], indent=2)[:500])
                
    else:
        print("ERROR: Could not find 'en' content in response")
else:
    print(f"ERROR: API returned status {response.status_code}")
    print(response.text[:500])
