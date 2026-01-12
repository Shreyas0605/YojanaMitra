
import json
from app import app, db, Scheme

karnataka_schemes = [
    # --- Energy & Water (Utilities) ---
    {
        "name": "Surya Raitha Scheme",
        "category": "Energy",
        "description": "Solar Water Pump set scheme for farmers to replace existing irrigation pumps.",
        "benefits": "Subsidized solar pumps, net metering for selling excess power.",
        "eligibility": "Farmers in Karnataka.",
        "allowedStates": ["Karnataka"],
        "allowedOccupations": ["Farmer"],
        "applicationLink": "https://bescom.karnataka.gov.in"
    },
    {
        "name": "Karnataka Ganga Kalyana Scheme",
        "category": "Water",
        "description": "Irrigation facility through lift irrigation or borewells for SC/ST/OBC farmers.",
        "benefits": "Drilling of borewells/open wells and energization.",
        "eligibility": "Small/Marginal farmers belonging to SC/ST/OBC involved in agriculture.",
        "allowedStates": ["Karnataka"],
        "allowedOccupations": ["Farmer"],
        "allowedCastes": ["SC", "ST", "OBC"],
        "applicationLink": "https://kmdc.karnataka.gov.in"
    },
    {
        "name": "Jalakhya Scheme",
        "category": "Water",
        "description": "Community based tank management to ensure water for agriculture.",
        "benefits": "Improved water availability.",
        "eligibility": "Village communities in Karnataka.",
        "allowedStates": ["Karnataka"],
        "residenceRequirement": "Rural",
        "applicationLink": "https://waterresources.karnataka.gov.in"
    },

    # --- Social Security ---
    {
        "name": "Sandhya Suraksha Yojana",
        "category": "Pension",
        "description": "Financial assistance to senior citizens.",
        "benefits": "Enhanced monthly pension mainly for weaker sections.",
        "eligibility": "Senior Citizens (65+), Income < 20,000.",
        "allowedStates": ["Karnataka"],
        "minAge": 65,
        "maxIncome": 20000,
        "applicationLink": "https://sevasindhu.karnataka.gov.in"
    },
    {
        "name": "Manasvini Scheme",
        "category": "Pension",
        "description": "Pension for unmarried poor women and divorced women.",
        "benefits": "Monthly pension assistance.",
        "eligibility": "Unmarried/Divorced women, Age 40-64, BPL.",
        "allowedStates": ["Karnataka"],
        "allowedGenders": ["Female"],
        "allowedMaritalStatus": ["Single", "Divorced"],
        "minAge": 40,
        "maxAge": 64,
        "applicationLink": "https://sevasindhu.karnataka.gov.in"
    },
    {
        "name": "Mythri Scheme",
        "category": "Pension",
        "description": "Monthly pension forTransgender persons.",
        "benefits": "₹600 - ₹1200 per month.",
        "eligibility": "Transgender persons resident in Karnataka.",
        "allowedStates": ["Karnataka"],
        "allowedGenders": ["Transgender"], # Note: Backend needs to handle this or map to 'Other'
        "applicationLink": "https://sevasindhu.karnataka.gov.in"
    },

    # --- Health & Nutrition ---
    {
        "name": "Mathru Purna Scheme",
        "category": "Healthcare",
        "description": "One nutritious meal daily for pregnant and lactating women.",
        "benefits": "Hot cooked meal at Anganwadi.",
        "eligibility": "Pregnant women and lactating mothers.",
        "allowedStates": ["Karnataka"],
        "allowedGenders": ["Female"],
        "applicationLink": "https://dwcd.karnataka.gov.in"
    },
    {
        "name": "Arogya Karnataka",
        "category": "Healthcare",
        "description": "Universal Health Coverage (Co-branded with Ayushman Bharat).",
        "benefits": "Financial protection for secondary and tertiary care.",
        "eligibility": "All residents of Karnataka (APL/BPL differentiated).",
        "allowedStates": ["Karnataka"],
        "applicationLink": "https://arogya.karnataka.gov.in"
    },
    {
        "name": "Jyothi Sanjeevini Scheme",
        "category": "Healthcare",
        "description": "Health insurance for State Government Employees.",
        "benefits": "Cashless treatment in empaneled hospitals.",
        "eligibility": "Karnataka Govt Employees and dependents.",
        "allowedStates": ["Karnataka"],
        "allowedOccupations": ["Govt Employee"],
        "applicationLink": "https://arogya.karnataka.gov.in"
    },

    # --- Entrepreneurship & Others ---
    {
        "name": "Udyogini Scheme",
        "category": "Business Loan",
        "description": "Subsidized loans for women entrepreneurs.",
        "benefits": "Loan up to ₹3 Lakhs, subsidy up to 30%.",
        "eligibility": "Women entrepreneurs, Income < 1.5 Lakhs.",
        "allowedStates": ["Karnataka"],
        "allowedGenders": ["Female"],
        "maxIncome": 150000,
        "applicationLink": "https://ksawd.karnataka.gov.in"
    },
    {
        "name": "Saptapadi Mass Marriage Scheme",
        "category": "Social Welfare",
        "description": "Govt sponsored mass marriages in Muzrai temples.",
        "benefits": "Financial assistance of ₹55,000 to the couple.",
        "eligibility": "Hindus marrying in selected temples.",
        "allowedStates": ["Karnataka"],
        "applicationLink": "https://karnatakadatacheck.com" 
    },
    {
        "name": "Airavata Scheme",
        "category": "Employment",
        "description": "Taxi aggregation scheme for SC/ST youth.",
        "benefits": "Subsidy for buying taxi/cab.",
        "eligibility": "SC/ST youth in Karnataka.",
        "allowedStates": ["Karnataka"],
        "allowedCastes": ["SC", "ST"],
        "applicationLink": "https://adcl.karnataka.gov.in"
    }
]

def add_karnataka_schemes():
    with app.app_context():
        count = 0
        print(f"Adding {len(karnataka_schemes)} Karnataka Utility & Welfare Schemes...")
        for s_data in karnataka_schemes:
            exists = Scheme.query.filter(Scheme.name.ilike(f"%{s_data['name']}%")).first()
            if not exists:
                scheme = Scheme(
                    name=s_data['name'],
                    description=s_data['description'],
                    category=s_data.get('category'),
                    benefits=s_data.get('benefits'),
                    eligibility=s_data.get('eligibility'),
                    application_link=s_data.get('applicationLink'),
                    allowed_states=json.dumps(s_data.get('allowedStates', [])),
                    allowed_occupations=json.dumps(s_data.get('allowedOccupations', [])),
                    allowed_castes=json.dumps(s_data.get('allowedCastes', [])),
                    allowed_genders=json.dumps(s_data.get('allowedGenders', [])),
                    allowed_marital_status=json.dumps(s_data.get('allowedMaritalStatus', [])),
                    min_age=s_data.get('minAge'),
                    max_age=s_data.get('maxAge'),
                    max_income=s_data.get('maxIncome'),
                    residence_requirement=s_data.get('residenceRequirement', 'Any'),
                    # Defaults
                    target_audience="Citizens",
                    allowed_education="[]",
                    disability_requirement="Any"
                )
                db.session.add(scheme)
                count += 1
            else:
                print(f"Skipping {s_data['name']} (Already exists)")
        
        # Verify 5 Guarantees Existence
        guarantees = ["Gruha Jyothi", "Gruha Lakshmi", "Shakti", "Anna Bhagya", "Yuva Nidhi"]
        print("\nVerifying 5 Guarantees:")
        for g in guarantees:
            found = Scheme.query.filter(Scheme.name.ilike(f"%{g}%")).first()
            if found:
                print(f"[OK] {g} is present.")
            else:
                print(f"[MISSING] {g} is MISSING!")

        db.session.commit()
        print(f"\nSuccessfully added {count} new Karnataka schemes.")

if __name__ == "__main__":
    add_karnataka_schemes()
