
import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

# --- Ground Truth Test Data ---
# We define a User Profile and the List of Schemes we EXPECT to see recommended.
TEST_CASES = [
    {
        "name": "Case 1: Young Girl for Sukanya Samriddhi",
        "profile": {
            "age": 5,
            "gender": "Female",
            "state": "Delhi",
            "income": 100000,
            "occupation": "Student",
            "caste": "General",
            "marital_status": "Single",
            "residence": "Urban"
        },
        "expected_schemes": ["Sukanya Samriddhi Yojana"], # Must have
        "excluded_schemes": ["PMSBY", "PMJJBY"] # Too young
    },
    {
        "name": "Case 2: Adult Male Farmer (PM Kisan)",
        "profile": {
            "age": 40,
            "gender": "Male",
            "state": "Maharashtra",
            "income": 200000,
            "occupation": "Farmer", # Triggers Farmer schemes
            "isFarmer": "Yes",
            "caste": "OBC",
            "marital_status": "Married",
            "residence": "Rural"
        },
        "expected_schemes": ["Kisan Credit Card (KCC)", "Soil Health Card Scheme"],
        "excluded_schemes": ["Sukanya Samriddhi Yojana"]
    },
    {
        "name": "Case 3: Senior Citizen (Pension)",
        "profile": {
            "age": 65,
            "gender": "Female",
            "state": "Karnataka",
            "income": 40000, # BPL likely
            "occupation": "Unemployed",
            "caste": "SC",
            "marital_status": "Widowed",
            "residence": "Rural",
            "isSeniorCitizen": "Yes",
            "isWidowSingleWoman": "Yes"
        },
        "expected_schemes": ["National Social Assistance Programme (NSAP) - Old Age Pension", "Rashtriya Vayoshri Yojana"],
        "excluded_schemes": ["Atal Pension Yojana"] # Max age 40
    },
    {
        "name": "Case 4: Student Sc/ST Scholarship",
        "profile": {
            "age": 20,
            "gender": "Male",
            "state": "Tamil Nadu",
            "income": 150000,
            "occupation": "Student",
            "caste": "SC",
            "education": "Graduate",
            "educationStatus": "Pursuing",
            "residence": "Urban"
        },
        "expected_schemes": ["Post Matric Scholarship for SC Students"],
        "excluded_schemes": []
    }
]

def evaluate():
    print("--------------------------------------------------")
    print("      YojanaMitra Accuracy Evaluation System      ")
    print("--------------------------------------------------")
    
    total_checks = 0
    passed_checks = 0
    
    for case in TEST_CASES:
        print(f"\nRunning {case['name']}...")
        profile = case['profile']
        expected = case.get('expected_schemes', [])
        excluded = case.get('excluded_schemes', [])
        
        try:
            # 1. Verification Request
            response = requests.post(f"{BASE_URL}/check-eligibility", json=profile)
            
            if response.status_code != 200:
                print(f"[ERROR] API Error: {response.status_code}")
                continue
                
            data = response.json()
            returned_schemes = [s['name'] for s in data.get('schemes', [])]
            
            # 2. Analyze Results
            case_passed = True
            
            # Check Expected (Recall)
            for exp in expected:
                total_checks += 1
                if exp in returned_schemes:
                    print(f"  [OK] Found expected: {exp}")
                    passed_checks += 1
                else:
                    print(f"  [FAIL] MISSED expected: {exp}")
                    case_passed = False

            # Check Excluded (Precision)
            for exc in excluded:
                total_checks += 1
                if exc not in returned_schemes:
                    print(f"  [OK] Correctly excluded: {exc}")
                    passed_checks += 1
                else:
                    print(f"  [FAIL] INCORRECTLY included: {exc}")
                    case_passed = False
                    
        except Exception as e:
            print(f"[ERROR] Exception: {e}")
            
    print("\n--------------------------------------------------")
    accuracy = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    print(f"Total Checks: {total_checks}")
    print(f"Passed Checks: {passed_checks}")
    print(f"SYSTEM ACCURACY: {accuracy:.2f}%")
    print("--------------------------------------------------")

if __name__ == "__main__":
    time.sleep(1) # Allow for startup if needed
    evaluate()
