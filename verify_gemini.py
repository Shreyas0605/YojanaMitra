
import sys
import os
import json

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

from app import app, db

def verify_gemini():
    print("Starting Gemini Verification...")
    
    # Create a test client
    with app.test_client() as client:
        # 1. Test without login (should get fallback or generic response)
        print("\n1. Testing Chat without Login...")
        response = client.post('/api/chat', json={'message': 'Hello'})
        print(f"Status: {response.status_code}")
        data = response.get_json()
        print(f"Response: {json.dumps(data, ensure_ascii=True)}")
        
        # 2. Test with Gemini (mocking session if needed, but app.py handles not logged in)
        # We want to see if 'powered_by' is 'gemini'
        print("\n2. Testing Chat with Gemini (General Query)...")
        response = client.post('/api/chat', json={'message': 'What is PM-KISAN?'})
        print(f"Status: {response.status_code}")
        data = response.get_json()
        print(f"Response: {json.dumps(data, ensure_ascii=True)}")
        
        if response.status_code == 200 and data.get('powered_by') == 'gemini':
            print("\nSUCCESS: Gemini API is responding!")
            return True
        else:
            print("\nFAILURE: Gemini API did not respond as expected.")
            if data.get('powered_by') == 'fallback':
                print("   (Fallback mechanism was used instead)")
            return False

if __name__ == "__main__":
    success = verify_gemini()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
