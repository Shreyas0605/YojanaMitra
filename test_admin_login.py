import requests

def test_login():
    url = 'http://127.0.0.1:5000/api/login'
    payload = {
        'email': 'admin@yojanamitra.in',
        'password': 'admin123'
    }
    
    try:
        session = requests.Session()
        print(f"Attempting login to {url}...")
        response = session.post(url, json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        print(f"Cookies: {session.cookies.get_dict()}")
        
        if response.status_code == 200:
            print("Login successful! Checking /api/admin/me...")
            # Check protected endpoint
            me_response = session.get('http://127.0.0.1:5000/api/admin/me')
            print(f"Me Status: {me_response.status_code}")
            print(f"Me Body: {me_response.text}")
        else:
            print("Login failed.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
