
import logging
import sys
import os

# Add current dir to path to allow imports
sys.path.append(os.getcwd())

from scheme_scraper import KarnatakaSevaSetheScraper, KarnatakaOneScraper, EducationGovInScraper

# Setup logging to print to console
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def debug_sevasethe():
    print("\n" + "="*50)
    print("DEBUGGING KARNATAKA SEVA SETHE")
    print("="*50)
    scraper = KarnatakaSevaSetheScraper("https://sevasindhu.karnataka.gov.in/Sevasindhu/DepartmentServices")
    
    print(f"Fetching: {scraper.source_url}")
    soup = scraper.fetch_page(scraper.source_url)
    
    if not soup:
        print("❌ Failed to fetch page")
        return

    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables")
    
    count = 0
    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        print(f"Table {i+1}: {len(rows)} rows")
        
        for j, row in enumerate(rows[:5]): # Print first 5 rows of each table
            cols = row.find_all('td')
            texts = [c.get_text(strip=True) for c in cols]
            print(f"  Row {j}: {texts}")
            
            # Check logic
            if len(cols) >= 2:
                # Try finding name in first 3 cols
                for k, col in enumerate(cols[:3]):
                    text = col.get_text(strip=True)
                    is_valid = scraper.is_valid_scheme_name(text)
                    print(f"    Col {k} Text: '{text}' | Valid: {is_valid}")
                    if is_valid:
                        count += 1
                        print(f"    ✅ MATCH: {text}")

    print(f"Total potential schemes found: {count}")

def debug_karnataka_one():
    print("\n" + "="*50)
    print("DEBUGGING KARNATAKA ONE")
    print("="*50)
    scraper = KarnatakaOneScraper("https://karnatakaone.gov.in/Public/Services")
    
    print(f"Fetching: {scraper.source_url}")
    soup = scraper.fetch_page(scraper.source_url)
    
    if not soup:
        print("❌ Failed to fetch page")
        return

    # Check for service items
    items = soup.find_all(['div', 'li', 'a'], class_=lambda x: x and 'service' in x.lower())
    print(f"Found {len(items)} items with class 'service'")
    
    for i, item in enumerate(items[:10]):
        text = item.get_text(strip=True)
        is_valid = scraper.is_valid_scheme_name(text)
        print(f"  Item {i}: '{text}' | Valid: {is_valid}")

    # Check tables
    tables = soup.find_all('table')
    print(f"Found {len(tables)} tables (Fallback)")
    
    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        print(f"Table {i+1}: {len(rows)} rows")
        for j, row in enumerate(rows[:5]):
            cols = row.find_all('td')
            texts = [c.get_text(strip=True) for c in cols]
            print(f"  Row {j}: {texts}")

if __name__ == "__main__":
    debug_sevasethe()
    debug_karnataka_one()
