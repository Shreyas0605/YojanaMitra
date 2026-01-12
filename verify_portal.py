
import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def test_portal():
    session = requests.Session()
    
    print("Starting Portal Verification...")

    # 1. Register
    print("\n1. Testing Registration...")
    reg_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "mobile": "1234567890"
    }
    # Clean up if exists (optional, or just handle error)
    res = session.post(f"{BASE_URL}/register", json=reg_data)
    if res.status_code == 201:
        print("Registration Successful")
    elif res.status_code == 400 and "already registered" in res.text:
        print("User already registered (Expected if re-running)")
    else:
        print(f"Registration Failed: {res.text}")
        return False

    # 2. Login
    print("\n2. Testing Login...")
    login_data = {"email": "test@example.com", "password": "password123"}
    res = session.post(f"{BASE_URL}/login", json=login_data)
    if res.status_code == 200:
        print("Login Successful")
    else:
        print(f"Login Failed: {res.text}")
        return False

    # 3. Profile Update
    print("\n3. Testing Profile Update...")
    profile_data = {
        "age": 30,
        "gender": "Male",
        "occupation": "Farmer",
        "income": 50000,
        "state": "Maharashtra",
        "caste": "General"
    }
    res = session.post(f"{BASE_URL}/profile", json=profile_data)
    if res.status_code == 200:
        print("Profile Update Successful")
    else:
        print(f"Profile Update Failed: {res.text}")
        return False

    # 4. Search Schemes
    print("\n4. Testing Scheme Search...")
    # Search for 'Farmer' (should match PM-KISAN)
    res = session.get(f"{BASE_URL}/schemes?q=farmer")
    if res.status_code == 200:
        schemes = res.json().get('schemes', [])
        if len(schemes) > 0:
            print(f"Search found {len(schemes)} schemes")
        else:
            print("Search returned 0 schemes (Check seed data)")
    else:
        print(f"Search Failed: {res.text}")
        return False

    print("\nAll Portal Tests Passed!")
    return True

if __name__ == "__main__":
    try:
        if test_portal():
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
