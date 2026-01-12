from scheme_scraper import MySchemeScraper
import json
import requests

scraper = MySchemeScraper("https://www.myscheme.gov.in/search")

slugs = ["ns-icarif", "icar-es"]
print(f"Testing extraction for slugs: {slugs}")

headers = {
    'User-Agent': scraper.session.headers['User-Agent'],
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.myscheme.gov.in',
    'Referer': 'https://www.myscheme.gov.in/',
    'x-api-key': 'tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc'
}

for slug in slugs:
    print(f"\n--- Testing SLUG: {slug} ---")
    detail_url = f"https://api.myscheme.gov.in/schemes/v6/public/schemes?slug={slug}&lang=en"

    try:
        resp = requests.get(detail_url, headers=headers, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            details_json = resp.json()
            
            # Application of current logic
            root = {}
            if isinstance(details_json, list) and details_json:
                root = details_json[0].get('en', {})
            elif isinstance(details_json, dict):
                if 'data' in details_json and isinstance(details_json['data'], dict):
                    root = details_json['data'].get('en', {})
                else:
                    root = details_json.get('en', {})
            
            if not root:
                print("FAILED: No 'en' content found.")
                continue

            basic = root.get('basicDetails', {})
            content = root.get('schemeContent', {})
            eligibility_criteria = root.get('eligibilityCriteria', {})
            
            def extract_text(data):
                if not data: return ''
                if isinstance(data, str): return data.strip()
                if isinstance(data, dict):
                    # Check for markdown fields first
                    for md_key in ['eligibilityDescription_md', 'benefits_md', 'description_md', 'content_md', 'text_md', 'applicationProcess_md', 'exclusions_md']:
                        if data.get(md_key): return data.get(md_key).strip()
                    
                    # Fallback to text fields
                    for text_key in ['description', 'text', 'content', 'label']:
                        val = data.get(text_key)
                        if val and isinstance(val, str): return val.strip()
                    
                    parts = []
                    for k, v in data.items():
                        if k not in ['type', 'mode', 'url', 'align']:
                            text = extract_text(v)
                            if text: parts.append(text)
                    return '\n'.join(parts)
                if isinstance(data, list):
                    parts = []
                    for item in data:
                        text = extract_text(item)
                        if text: parts.append(text)
                    return '\n'.join(parts)
                return str(data)

            benefits = content.get('benefits_md') or extract_text(content.get('benefits', [])) or 'Refer to portal'
            eligibility = extract_text(eligibility_criteria) or 'Refer to portal'
            
            print(f"NAME: {basic.get('schemeName')}")
            print(f"BENEFITS (first 100): {benefits[:100]}...")
            print(f"ELIGIBILITY (first 100): {eligibility[:100]}...")
            
            if benefits == 'Refer to portal':
                 print(f"DEBUG content['benefits']: {content.get('benefits')}")
    except Exception as e:
        print(f"Error test: {e}")
