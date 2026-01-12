
import requests
import json
import warnings
warnings.filterwarnings("ignore")

base_urls = [
    "https://sevasindhu.karnataka.gov.in/api/dept",
    "https://sevasindhu.karnataka.gov.in/Sevasindhu/api/dept",
    "https://sevasindhu.karnataka.gov.in/Services/api/dept",
    "https://sevasindhu.karnataka.gov.in/api/Dept",  # Case sensitivity?
    "https://sevasindhu.karnataka.gov.in/Sevasindhu/api/Dept"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://sevasindhu.karnataka.gov.in/Sevasindhu/DepartmentServices'
}

print("Probing SevaSindhu API endpoints...")

for url in base_urls:
    print(f"\nTesting: {url}")
    try:
        resp = requests.get(url, headers=headers, verify=False, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            try:
                data = resp.json()
                print(f"✅ SUCCESS! Found {len(data)} items.")
                print("First item:", data[0] if data else "Empty list")
                break # Found it!
            except:
                print("❌ HTML response (not JSON)")
                print(resp.text[:100])
        else:
            print("❌ Failed")
    except Exception as e:
        print(f"Error: {e}")
