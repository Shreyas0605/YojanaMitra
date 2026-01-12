import requests
import json

try:
    print("Testing /api/schemes endpoint...")
    url = "http://localhost:5000/api/schemes"
    params = {
        'page': 1,
        'limit': 2,
        'category': 'All',
        'state': 'All',
        'q': ''
    }
    response = requests.get(url, params=params)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Keys in response: {list(data.keys())}")
        print(f"Total Items: {data.get('total_items')}")
        print(f"Page: {data.get('page')}")
        print(f"Number of schemes returned: {len(data.get('schemes', []))}")
        
        if data.get('schemes'):
            print("First scheme sample:")
            print(json.dumps(data['schemes'][0], indent=2))
        else:
            print("No schemes found in 'schemes' list.")
            
            # Additional debug: Check what happens with minimal params
            print("\nRetrying with NO params...")
            response_raw = requests.get(url)
            data_raw = response_raw.json()
            print(f"Total Items (Raw): {data_raw.get('total_items')}")
            print(f"Schemes (Raw): {len(data_raw.get('schemes', []))}")
            
    else:
        print("Error: Non-200 status code")
        print(response.text)

except Exception as e:
    print(f"Script failed: {e}")
