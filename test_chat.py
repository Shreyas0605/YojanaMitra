import requests
import json
import time

def test_chat():
    url = "http://localhost:5000/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {"message": "Hello, tell me about PM Kisan scheme"}
    
    print(f"Testing Chatbot API at {url}...")
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200 and 'response' in response.json():
            print("\n[PASS] Chatbot test PASSED!")
        else:
            print("\n[FAIL] Chatbot test FAILED!")
            
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")

if __name__ == "__main__":
    # Wait a bit for server to start
    time.sleep(3)
    test_chat()
