import requests
import json

BASE_URL = "http://localhost:5000"

def verify_conflict():
    # Profile that matches BOTH schemes
    # Scheme 19 (SC Post Matric): Needs Caste=SC, Income < 2.5L
    # Scheme 42 (Disability): Needs Disability=Yes, Disability% > 40
    
    profile = {
        "age": 20,
        "state": "Karnataka",
        "caste": "SC",
        "income": 50000,
        "disability": "Yes",
        "disabilityPercentage": 60,
        "occupation": "Student",
        "gender": "Male"
    }
    
    print("Sending profile to /api/check-eligibility...")
    try:
        response = requests.post(f"{BASE_URL}/api/check-eligibility", json=profile)
        response.raise_for_status()
        data = response.json()
        
        schemes = data.get('schemes', [])
        print(f"Found {len(schemes)} eligible schemes.")
        
        # Check for our specific schemes
        s19 = next((s for s in schemes if s['id'] == 19), None)
        s42 = next((s for s in schemes if s['id'] == 42), None)
        
        if s19:
            print(f"Found Scheme 19: {s19['name']}")
            print(f"  Conflicts: {s19.get('conflicts')}")
        else:
            print("Scheme 19 NOT found (Unexpected).")
            
        if s42:
            print(f"Found Scheme 42: {s42['name']}")
            print(f"  Conflicts: {s42.get('conflicts')}")
        else:
            print("Scheme 42 NOT found (Unexpected).")
            
        # Assertion
        if s19 and s42:
            if s19.get('conflicts') and s42.get('conflicts'):
                print("\nSUCCESS: Both schemes identified each other as conflicts.")
            else:
                print("\nFAILURE: Conflict data missing.")
        else:
            print("\nFAILURE: Did not match both schemes to test conflict.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_conflict()
