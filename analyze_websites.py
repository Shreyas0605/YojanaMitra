"""
Analyze the HTML structure of Karnataka government websites to build working scrapers
"""

import requests
from bs4 import BeautifulSoup
import json

def analyze_website(url, name):
    """Fetch and analyze the HTML structure of a website"""
    print(f"\n{'='*60}")
    print(f"Analyzing: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print(f"Successfully fetched (Status: {response.status_code})")
        print(f"Content length: {len(response.content)} bytes")
        
        # Save full HTML for manual inspection
        filename = f"analysis_{name.replace(' ', '_').lower()}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"Saved HTML to: {filename}")
        
        # Look for common patterns
        print("\nLooking for potential scheme containers...")
        
        # Try to find tables
        tables = soup.find_all('table')
        print(f"  - Found {len(tables)} tables")
        
        # Try to find cards/divs with class containing 'scheme', 'card', 'item'
        scheme_containers = soup.find_all(['div', 'article', 'section'], 
                                         class_=lambda x: x and any(word in x.lower() for word in ['scheme', 'card', 'item', 'service', 'yojana']))
        print(f"  - Found {len(scheme_containers)} potential scheme containers")
        
        # Try to find links with scheme-related keywords
        links = soup.find_all('a', href=True)
        scheme_links = [l for l in links if any(word in l.get_text().lower() for word in ['scheme', 'yojana', 'service', 'benefit'])]
        print(f"  - Found {len(scheme_links)} scheme-related links (out of {len(links)} total links)")
        
        if scheme_links:
            print("\n  Sample scheme links:")
            for link in scheme_links[:5]:
                print(f"    - {link.get_text().strip()[:60]}")
                print(f"      URL: {link.get('href')[:80]}")
        
        # Look for headings
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        print(f"  - Found {len(headings)} headings")
        
        if headings:
            print("\n  Sample headings:")
            for h in headings[:10]:
                text = h.get_text().strip()
                if text:
                    print(f"    - {h.name}: {text[:80]}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    # Analyze specific service pages found
    websites = [
        ("https://sevasindhu.karnataka.gov.in/Sevasindhu/DepartmentServices", "SevaSindhu Services"),
        ("https://karnatakaone.gov.in/Public/Services", "Karnataka One Services"),
        # NSP URL might need adjustment, checking main page again or specific section if possible
        # "All-Scholarships" might be a fragment or dynamic. Let's try to stick to main or find a better one.
        # Actually https://scholarships.gov.in/ often has specific sections. 
        # But let's check the ones we found.
    ]
    
    for url, name in websites:
        analyze_website(url, name)
        print("\n")
