
import json
from app import app, db, Scheme

karnataka_scholarships = [
    # --- SSP (State Scholarship Portal) Karnataka Schemes ---
    {
        "name": "SSP Post-Matric Scholarship (Karnataka)",
        "category": "Education",
        "description": "Unified state scholarship for SC/ST/OBC/Minority students pursuing post-matric education (Class 11 to Ph.D).",
        "benefits": "Tuition fee reimbursement and maintenance allowance.",
        "eligibility": "Students of Karnataka, Income limits apply (vary by caste).",
        "allowedStates": ["Karnataka"],
        "allowedOccupations": ["Student"],
        "applicationLink": "https://ssp.postmatric.karnataka.gov.in"
    },
    {
        "name": "Vidyasiri (Food & Accommodation)",
        "category": "Education",
        "description": "Assistance for students from backward classes who have not got admission in government hostels.",
        "benefits": "₹1,500 per month for 10 months.",
        "eligibility": "BC/OBC students in Karnataka, Rural/Urban distance criteria.",
        "allowedStates": ["Karnataka"],
        "allowedOccupations": ["Student"],
        "allowedCastes": ["OBC", "SC", "ST"],
        "applicationLink": "https://bcwd.karnataka.gov.in"
    },
    {
        "name": "Raita Vidya Nidhi Scholarship",
        "category": "Education",
        "description": "Chief Minister's Raita Vidya Nidhi scholarship for children of farmers.",
        "benefits": "₹2,000 to ₹11,000 per year depending on course.",
        "eligibility": "Children of Farmers in Karnataka.",
        "allowedStates": ["Karnataka"],
        "allowedOccupations": ["Student"],
        "isFarmer": "Yes", # Custom logic field match
        "applicationLink": "https://ssp.postmatric.karnataka.gov.in"
    },
    {
        "name": "Sanchi Honnamma Scholarship",
        "category": "Education",
        "description": "Scholarship to encourage girl students pursuing general non-professional degrees.",
        "benefits": "₹2,000 per annum.",
        "eligibility": "Meritorious girl students in Karnataka.",
        "allowedStates": ["Karnataka"],
        "allowedGenders": ["Female"],
        "allowedOccupations": ["Student"],
        "applicationLink": "https://dce.karnataka.gov.in"
    },
    {
        "name": "Sir C.V. Raman Scholarship",
        "category": "Education",
        "description": "Scholarship for students pursuing Basic Sciences (B.Sc, M.Sc).",
        "benefits": "₹5,000/month (varies) to encourage basic science education.",
        "eligibility": "Students enrolled in Basic Sciences in Karnataka.",
        "allowedStates": ["Karnataka"],
        "allowedOccupations": ["Student"],
        "applicationLink": "https://dce.karnataka.gov.in"
    },
    {
        "name": "Karnataka Labour Welfare Board Scholarship",
        "category": "Education",
        "description": "Scholarship for children of organized sector workers.",
        "benefits": "Financial assistance for education from High School to Degree.",
        "eligibility": "Children of workers contributing to Labour Welfare Fund.",
        "allowedStates": ["Karnataka"],
        "allowedOccupations": ["Student"],
        "applicationLink": "https://klwbapps.karnataka.gov.in"
    },
    {
        "name": "Fee Reimbursement Scheme (Karnataka)",
        "category": "Education",
        "description": "Full fee reimbursement for engineerig and medical students.",
        "benefits": "Complete waiver of tuition fees.",
        "eligibility": "SC/ST students in Karnataka with income < 2.5 Lakhs.",
        "allowedStates": ["Karnataka"],
        "allowedOccupations": ["Student"],
        "allowedCastes": ["SC", "ST"],
        "maxIncome": 250000,
        "applicationLink": "https://ssp.postmatric.karnataka.gov.in"
    },
    
    # --- NSP (National Scholarship Portal) Popular in Karnataka ---
    {
        "name": "Central Sector Scheme of Scholarship (CSS)",
        "category": "Education",
        "description": "Scholarship for College and University Students involved in General/Professional courses.",
        "benefits": "₹10,000 to ₹20,000 per annum.",
        "eligibility": "Above 80th percentile in Class 12, Income < 8 Lakhs.",
        "allowedOccupations": ["Student"],
        "maxIncome": 800000,
        "applicationLink": "https://scholarships.gov.in"
    },
    {
        "name": "NSP Merit Cum Means Scholarship (Professional)",
        "category": "Education",
        "description": "For students belonging to minority communities pursuing professional/technical courses.",
        "benefits": "Course fee reimbursement + Maintenance allowance.",
        "eligibility": "Minorities (Muslim, Christian, Sikh, etc.), >50% marks, Income < 2.5 Lakhs.",
        "allowedOccupations": ["Student"],
        "maxIncome": 250000,
        "minorityStatus": "Yes",
        "applicationLink": "https://scholarships.gov.in"
    },
    {
        "name": "AICTE Pragati Scholarship for Girls",
        "category": "Education",
        "description": "Scholarship for girl students admitting in Technical Degree/Diploma.",
        "benefits": "₹50,000 per annum.",
        "eligibility": "Girl students in AICTE approved institutions.",
        "allowedGenders": ["Female"],
        "allowedOccupations": ["Student"],
        "applicationLink": "https://scholarships.gov.in"
    },
    {
        "name": "AICTE Saksham Scholarship (Disabled)",
        "category": "Education",
        "description": "Scholarship for differently-abled students for technical education.",
        "benefits": "₹50,000 per annum.",
        "eligibility": "Differently-abled students (>40%) in technical courses.",
        "disabilityRequirement": "Yes",
        "allowedOccupations": ["Student"],
        "applicationLink": "https://scholarships.gov.in"
    },
    {
        "name": "Post Matric Scholarship for Minorities (NSP)",
        "category": "Education",
        "description": "Scholarship for minority students from Class 11 to Ph.D.",
        "benefits": "Admission + Tuition fee + Maintenance.",
        "eligibility": "Minorities, >50% marks, Income < 2 Lakhs.",
        "allowedOccupations": ["Student"],
        "minorityStatus": "Yes",
        "maxIncome": 200000,
        "applicationLink": "https://scholarships.gov.in"
    },
    # --- Other Karnataka Specific ---
    {
        "name": "Kitur Rani Chennamma Award",
        "category": "Education",
        "description": "Award for meritorious girl students.",
        "benefits": "Cash prize.",
        "eligibility": "Girl students passing SSLC/PUC with high marks.",
        "allowedStates": ["Karnataka"],
        "allowedGenders": ["Female"],
        "allowedOccupations": ["Student"],
        "applicationLink": "https://dce.karnataka.gov.in"
    },
    {
        "name": "Arivu Education Loan Scheme",
        "category": "Education",
        "description": "Education loan for minority students for professional courses.",
        "benefits": "Loan up to ₹3 Lakhs at 2% interest.",
        "eligibility": "Minority students in Karnataka (KMDC).",
        "allowedStates": ["Karnataka"],
        "minorityStatus": "Yes",
        "allowedOccupations": ["Student"],
        "applicationLink": "https://kmdc.karnataka.gov.in"
    }
]

def add_scholarships():
    with app.app_context():
        count = 0
        print(f"Adding {len(karnataka_scholarships)} Student Scholarships...")
        for s_data in karnataka_scholarships:
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
                    max_income=s_data.get('maxIncome'),
                    disability_requirement=s_data.get('disabilityRequirement', 'Any'),
                    # Defaults
                    target_audience="Students",
                    allowed_education="[]",
                    allowed_marital_status="[]",
                    residence_requirement="Any",
                    min_age=16, # Default for these
                    max_age=30
                )
                db.session.add(scheme)
                count += 1
            else:
                print(f"Skipping {s_data['name']} (Already exists)")
        
        db.session.commit()
        print(f"Successfully added {count} new scholarships.")

if __name__ == "__main__":
    add_scholarships()
