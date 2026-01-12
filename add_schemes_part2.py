
import json
from app import app, db, Scheme

more_schemes = []

# Generate specific trade-based schemes for Vishwakarma sub-categories
trades = [
    "Carpenter (Suthar)", "Boat Maker", "Armourer", "Blacksmith (Lohar)", 
    "Hammer and Tool Kit Maker", "Locksmith", "Goldsmith (Sonar)", "Potter (Kumhaar)",
    "Sculptor (Moortikar)", "Cobbler (Charmakar)", "Mason (Rajmistri)", 
    "Basket/Mat/Broom Maker", "Doll & Toy Maker", "Barber (Naai)", 
    "Garland Maker (Malakaar)", "Washerman (Dhobi)", "Tailor (Darzi)", 
    "Fishing Net Maker"
]

for trade in trades:
    more_schemes.append({
        "name": f"PM Vishwakarma - {trade} Support",
        "category": "Skill Development",
        "description": f"Dedicated support for artisans working as {trade}.",
        "benefits": "Toolkit incentive of ₹15,000 + Collateral free loans.",
        "eligibility": f"Traditional artisans in {trade} trade.",
        "minAge": 18,
        "applicationLink": "https://pmvishwakarma.gov.in"
    })

# Additional specific state schemes (Northeast & Others)
northeast_states = ["Manipur", "Meghalaya", "Mizoram", "Nagaland", "Tripura", "Sikkim", "Arunachal Pradesh"]
for state in northeast_states:
    more_schemes.append({
        "name": f"{state} Entrepreneurship Mission",
        "category": "Business",
        "description": f"Support for entrepreneurs in {state}.",
        "benefits": "Seed funding up to ₹5 Lakhs.",
        "eligibility": f"Residents of {state}.",
        "allowedStates": [state],
        "applicationLink": f"https://startup.{state.lower().replace(' ', '')}.gov.in"
    })

def add_more_schemes():
    with app.app_context():
        count = 0
        print(f"Adding {len(more_schemes)} supplemental schemes...")
        for s_data in more_schemes:
            exists = Scheme.query.filter(Scheme.name.ilike(f"%{s_data['name']}%")).first()
            if not exists:
                scheme = Scheme(
                    name=s_data['name'],
                    description=s_data['description'],
                    category=s_data.get('category'),
                    benefits=s_data.get('benefits'),
                    eligibility=s_data.get('eligibility'),
                    application_link=s_data.get('applicationLink'),
                    min_age=s_data.get('minAge'),
                    max_age=s_data.get('maxAge'),
                    allowed_states=json.dumps(s_data.get('allowedStates', [])),
                    # Defaults
                    target_audience="Citizens",
                    allowed_genders="[]",
                    allowed_occupations="[]",
                    allowed_castes="[]",
                    allowed_education="[]",
                    allowed_marital_status="[]",
                    disability_requirement="Any",
                    residence_requirement="Any"
                )
                db.session.add(scheme)
                count += 1
            else:
                pass
        
        db.session.commit()
        print(f"Successfully added {count} more schemes.")

if __name__ == "__main__":
    add_more_schemes()
