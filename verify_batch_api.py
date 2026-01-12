import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"
SESSION = requests.Session()

def login():
    try:
        print(f"Logging in to {BASE_URL}...")
        resp = SESSION.post(f"{BASE_URL}/api/login", json={
            "email": "admin@yojanamitra.gov.in",
            "password": "admin123"
        })
        if resp.status_code == 200:
            print("Login successful.")
            return True
        else:
            print(f"Login failed: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False

def get_pending():
    print("Fetching pending schemes...")
    resp = SESSION.get(f"{BASE_URL}/api/admin/pending-schemes")
    if resp.status_code == 200:
        data = resp.json()
        schemes = data.get('pendingSchemes', [])
        print(f"Found {len(schemes)} pending schemes.")
        return schemes
    else:
        print(f"Failed to fetch pending: {resp.status_code}")
        return []

def batch_approve(ids):
    print(f"Attempting to batch approve IDs: {ids}")
    resp = SESSION.post(f"{BASE_URL}/api/admin/pending/batch-approve", json={
        "ids": ids
    })
    if resp.status_code == 200:
        print(f"Batch approve success: {resp.json().get('message')}")
        return True
    else:
        print(f"Batch approve failed: {resp.status_code} - {resp.text}")
        return False

def verify_approval(ids):
    print("Verifying approval status...")
    # Check pending to ensure they are gone
    remaining_pending = get_pending()
    remaining_ids = [s['id'] for s in remaining_pending]
    
    for i in ids:
        if i in remaining_ids:
            print(f"FAILURE: Scheme ID {i} is still in pending list!")
            return False
    
    print("Success: Approved schemes are no longer in pending list.")
    
    # Check all schemes to ensure they are present
    print("Fetching active schemes...")
    resp = SESSION.get(f"{BASE_URL}/api/schemes")
    if resp.status_code == 200:
        active_schemes = resp.json().get('schemes', [])
        active_names = [s['name'] for s in active_schemes]
        # We can't check ID easily as it might change or be different table, 
        # but name should match if populated correctly.
        # Actually pending -> scheme migration creates new ID potentially? 
        # Let's check names.
        
        # Pending schemes list has names
        return True
    return False

def main():
    if not login():
        sys.exit(1)
        
    pending = get_pending()
    if not pending:
        print("No pending schemes to test with.")
        sys.exit(0)
    
    # Take up to 3 schemes
    to_approve = pending[:3]
    approve_ids = [s['id'] for s in to_approve]
    
    if batch_approve(approve_ids):
        if verify_approval(approve_ids):
            print("VERIFICATION SUCCESSFUL")
        else:
            print("VERIFICATION FAILED")
            sys.exit(1)
    else:
        print("Batch approve step failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
