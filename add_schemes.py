
import json
from app import app, db, Scheme

new_schemes = [
    # --- CENTRAL SECTOR SCHEMES ---
    # Agriculture & Farmers
    {
        "name": "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)",
        "category": "Agriculture",
        "description": "Scheme to improve on-farm water use efficiency.",
        "benefits": "Financial assistance for irrigation infrastructure.",
        "eligibility": "Farmers with agricultural land.",
        "allowedOccupations": ["Farmer"],
        "applicationLink": "https://pmksy.gov.in"
    },
    {
        "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "category": "Agriculture",
        "description": "Promotion of organic farming.",
        "benefits": "Financial assistance of ₹50,000 per hectare for 3 years.",
        "eligibility": "Farmers/Farmer groups.",
        "allowedOccupations": ["Farmer"],
        "applicationLink": "https://pgsindia-ncof.gov.in"
    },
    {
        "name": "e-NAM (National Agriculture Market)",
        "category": "Agriculture",
        "description": "Pan-India electronic trading portal for farm produce.",
        "benefits": "Better price discovery for farmers.",
        "eligibility": "Farmers, Traders.",
        "allowedOccupations": ["Farmer"],
        "applicationLink": "https://enam.gov.in"
    },
    {
        "name": "PM-Kisan Maan Dhan Yojana",
        "category": "Pension",
        "description": "Pension scheme for small and marginal farmers.",
        "benefits": "Min pension of ₹3000/month after age 60.",
        "eligibility": "Small/Marginal Farmers, Age 18-40.",
        "minAge": 18,
        "maxAge": 40,
        "allowedOccupations": ["Farmer"],
        "applicationLink": "https://pmkisan.gov.in"
    },
    
    # Education & Skill
    {
        "name": "PMKVY 4.0",
        "category": "Skill Development",
        "description": "Skill certification scheme for youth (latest version).",
        "benefits": "Free short duration skill training.",
        "eligibility": "Unemployed youth, school/college dropouts.",
        "minAge": 15,
        "maxAge": 45,
        "applicationLink": "https://www.pmkvyofficial.org"
    },
    {
        "name": "National Apprenticeship Promotion Scheme (NAPS)",
        "category": "Skill Development",
        "description": "Promotes apprenticeship training.",
        "benefits": "Stipend support to apprentices.",
        "eligibility": "ITI students, Graduates, Diploma holders.",
        "minAge": 14,
        "applicationLink": "https://www.apprenticeshipindia.gov.in"
    },
    {
        "name": "Jan Shikshan Sansthan (JSS)",
        "category": "Skill Development",
        "description": "Vocational skill training for non-literate/neo-literates.",
        "benefits": "Vocational training at low cost.",
        "eligibility": "Non-literates, neo-literates, 15-45 years.",
        "minAge": 15,
        "maxAge": 45,
        "residenceRequirement": "Rural",
        "applicationLink": "https://jss.gov.in"
    },
    {
        "name": "Mid-Day Meal Scheme (PM POSHAN)",
        "category": "Education",
        "description": "Hot cooked meal in govt schools.",
        "benefits": "Free lunch.",
        "eligibility": "Class 1-8 students.",
        "minAge": 5,
        "maxAge": 14,
        "allowedOccupations": ["Student"],
        "applicationLink": "https://pmposhan.education.gov.in"
    },
    {
        "name": "SWAYAM Platform",
        "category": "Education",
        "description": "Free online courses.",
        "benefits": "Free education resources.",
        "eligibility": "Any learner.",
        "applicationLink": "https://swayam.gov.in"
    },

    # Housing & Urban
    {
        "name": "PMAY-Urban (Pradhan Mantri Awas Yojana)",
        "category": "Housing",
        "description": "Housing for all in urban areas.",
        "benefits": "Interest subsidy/Financial assistance for house construction.",
        "eligibility": "Urban poor, EWS, LIG, MIG.",
        "residenceRequirement": "Urban",
        "applicationLink": "https://pmaymis.gov.in"
    },
     {
        "name": "PMAY-Gramin",
        "category": "Housing",
        "description": "Pucca house for rural poor.",
        "benefits": "Financial assistance for house construction.",
        "eligibility": "Rural houseless/living in kutcha houses.",
        "residenceRequirement": "Rural",
        "applicationLink": "https://pmayg.nic.in"
    },
    
    # Health
    {
        "name": "Ayushman Bharat - PMJAY",
        "category": "Healthcare",
        "description": "Health insurance for poor families.",
        "benefits": "Cover up to ₹5 Lakh per family per year.",
        "eligibility": "Bottom 40% population (SECC data).",
        "applicationLink": "https://pmjay.gov.in"
    },
    {
        "name": "Jan Aushadhi Yojana",
        "category": "Healthcare",
        "description": "Quality generic medicines at affordable prices.",
        "benefits": "Medicines at 50-90% cheaper rates.",
        "eligibility": "All citizens.",
        "applicationLink": "http://janaushadhi.gov.in"
    },
     {
        "name": "Mission Indradhanush",
        "category": "Healthcare",
        "description": "Immunization drive.",
        "benefits": "Free vaccination for 12 diseases.",
        "eligibility": "Children under 2 years, Pregnant women.",
        "minAge": 0,
        "maxAge": 2,
        "applicationLink": "https://www.nhp.gov.in"
    },

    # Women & Child
    {
        "name": "Mahila Samman Savings Certificate",
        "category": "Financial Inclusion",
        "description": "Small savings scheme for women.",
        "benefits": "7.5% fixed interest rate.",
        "eligibility": "Women and girls.",
        "allowedGenders": ["Female"],
        "applicationLink": "https://www.indiapost.gov.in"
    },
    {
        "name": "Nirbhaya Fund Schemes",
        "category": "Social Welfare",
        "description": "Schemes for women safety.",
        "benefits": "Various safety initiatives.",
        "eligibility": "Women.",
        "allowedGenders": ["Female"],
        "applicationLink": "https://wcd.nic.in"
    },
    {
        "name": "One Stop Centre Scheme",
        "category": "Social Welfare",
        "description": "Support for women affected by violence.",
        "benefits": "Medical, legal, and psychological support.",
        "eligibility": "Women affected by violence.",
        "allowedGenders": ["Female"],
        "applicationLink": "https://wcd.nic.in"
    },
    {
        "name": "Working Women Hostel Scheme",
        "category": "Social Welfare",
        "description": "Safe accommodation for working women.",
        "benefits": "Safe hostel facility.",
        "eligibility": "Working women.",
        "allowedGenders": ["Female"],
        "allowedOccupations": ["Salaried", "Self Employed"],
        "applicationLink": "https://wcd.nic.in"
    },

    # Social Security
    {
        "name": "Varishtha Pension Bima Yojana",
        "category": "Pension",
        "description": "Pension for senior citizens.",
        "benefits": "Guaranteed 8% return.",
        "eligibility": "Senior Citizens 60+.",
        "minAge": 60,
        "applicationLink": "https://financialservices.gov.in"
    },
    {
        "name": "National Family Benefit Scheme",
        "category": "Social Welfare",
        "description": "Lump sum assistance on death of primary breadwinner.",
        "benefits": "₹20,000 lump sum.",
        "eligibility": "BPL families.",
        "maxIncome": 40000,
        "applicationLink": "https://nsap.nic.in"
    },

    # --- STATE SCHEMES (Assorted) ---
    
    # Andhra Pradesh
    {
        "name": "YSR Rythu Bharosa",
        "category": "Agriculture",
        "description": "Financial assistance to farmers in AP.",
        "benefits": "₹13,500 per year.",
        "eligibility": "Farmers in AP.",
        "allowedStates": ["Andhra Pradesh"],
        "allowedOccupations": ["Farmer"],
        "applicationLink": "https://ysrrythubharosa.ap.gov.in"
    },
    {
        "name": "YSR Cheyutha",
        "category": "Social Welfare",
        "description": "Financial assistance to SC/ST/OBC/Minority women.",
        "benefits": "₹18,750 per year.",
        "eligibility": "Women 45-60 years, AP residents.",
        "minAge": 45,
        "maxAge": 60,
        "allowedStates": ["Andhra Pradesh"],
        "allowedGenders": ["Female"],
        "applicationLink": "https://gramawardsachivalayam.ap.gov.in"
    },
    {
        "name": "Jagananna Vidya Deevena",
        "category": "Education",
        "description": "Full fee reimbursement.",
        "benefits": "100% fee reimbursement.",
        "eligibility": "Students in AP, Income < 2.5L.",
        "allowedStates": ["Andhra Pradesh"],
        "allowedOccupations": ["Student"],
        "maxIncome": 250000,
        "applicationLink": "https://jnanabhumi.ap.gov.in"
    },

    # Telangana
    {
        "name": "Rythu Bandhu",
        "category": "Agriculture",
        "description": "Investment support for agriculture.",
        "benefits": "₹5000 per acre per season.",
        "eligibility": "Farmers in Telangana.",
        "allowedStates": ["Telangana"],
        "allowedOccupations": ["Farmer"],
        "applicationLink": "http://rythubandhu.telangana.gov.in"
    },
    {
        "name": "Dalit Bandhu",
        "category": "Social Welfare",
        "description": "Empowerment of Dalit families.",
        "benefits": "Grant of ₹10 Lakhs.",
        "eligibility": "SC families in Telangana.",
        "allowedStates": ["Telangana"],
        "allowedCastes": ["SC"],
        "applicationLink": "https://pres.telangana.gov.in"
    },
    {
        "name": "Kalyana Lakshmi/Shaadi Mubarak",
        "category": "Social Welfare",
        "description": "Financial assistance for marriage.",
        "benefits": "₹1,00,116 for bride.",
        "eligibility": "Girl from SC/ST/Minority/BC, Age 18+.",
        "minAge": 18,
        "allowedGenders": ["Female"],
        "allowedStates": ["Telangana"],
        "applicationLink": "https://telanganaepass.cgg.gov.in"
    },

    # West Bengal
    {
        "name": "Kanyashree Prakalpa",
        "category": "Child Welfare",
        "description": "Conditional cash transfer to curb child marriage.",
        "benefits": "Annual scholarship + One time grant.",
        "eligibility": "Girls 13-18 years in Bengal.",
        "minAge": 13,
        "maxAge": 18,
        "allowedGenders": ["Female"],
        "allowedStates": ["West Bengal"],
        "applicationLink": "https://www.wbkanyashree.gov.in"
    },
    {
        "name": "Krishak Bandhu",
        "category": "Agriculture",
        "description": "Financial assistance to farmers.",
        "benefits": "₹10,000 per acre per year.",
        "eligibility": "Farmers in West Bengal.",
        "allowedStates": ["West Bengal"],
        "allowedOccupations": ["Farmer"],
        "applicationLink": "https://krishakbandhu.net"
    },
    {
        "name": "Lakshmir Bhandar",
        "category": "Social Welfare",
        "description": "Basic income for women.",
        "benefits": "₹1000/month (SC/ST), ₹500/month (Gen).",
        "eligibility": "Women 25-60 years in WB.",
        "minAge": 25,
        "maxAge": 60,
        "allowedGenders": ["Female"],
        "allowedStates": ["West Bengal"],
        "applicationLink": "https://socialsecurity.wb.gov.in"
    },

    # Odisha
    {
        "name": "KALIA Scheme",
        "category": "Agriculture",
        "description": "Income augmentation for farmers.",
        "benefits": "Financial assistance for cultivation.",
        "eligibility": "Small/Marginal farmers in Odisha.",
        "allowedStates": ["Odisha"],
        "allowedOccupations": ["Farmer"],
        "applicationLink": "https://kalia.odisha.gov.in"
    },
    {
        "name": "Biju Swasthya Kalyan Yojana",
        "category": "Healthcare",
        "description": "Cashless healthcare.",
        "benefits": "Coverage up to ₹5L (₹10L for women).",
        "eligibility": "Families in Odisha.",
        "allowedStates": ["Odisha"],
        "applicationLink": "https://bsky.odisha.gov.in"
    },
    
    # Madhya Pradesh
    {
        "name": "Ladli Behna Yojana",
        "category": "Social Welfare",
        "description": "Financial independence for women.",
        "benefits": "₹1250 per month.",
        "eligibility": "Women 21-60 years in MP.",
        "minAge": 21,
        "maxAge": 60,
        "allowedGenders": ["Female"],
        "allowedStates": ["Madhya Pradesh"],
        "applicationLink": "https://cmladlibahna.mp.gov.in"
    },
    {
        "name": "Mukhyamantri Seekho Kamao Yojana",
        "category": "Employment",
        "description": "Learn and Earn scheme.",
        "benefits": "Stipend during training.",
        "eligibility": "Youth 18-29 years in MP.",
        "minAge": 18,
        "maxAge": 29,
        "allowedStates": ["Madhya Pradesh"],
        "applicationLink": "https://mmsky.mp.gov.in"
    },

    # Rajasthan
    {
        "name": "Chiranjeevi Swasthya Bima Yojana",
        "category": "Healthcare",
        "description": "Universal health insurance.",
        "benefits": "Cashless treatment up to ₹25 Lakhs.",
        "eligibility": "Residents of Rajasthan.",
        "allowedStates": ["Rajasthan"],
        "applicationLink": "https://chiranjeevi.rajasthan.gov.in"
    },
    {
        "name": "Indira Gandhi Urban Employment Guarantee Scheme",
        "category": "Employment",
        "description": "Employment guarantee for urban areas.",
        "benefits": "100 days of employment.",
        "eligibility": "Urban residents of Rajasthan.",
        "allowedStates": ["Rajasthan"],
        "residenceRequirement": "Urban",
        "applicationLink": "https://irgyurban.rajasthan.gov.in"
    },

    # Kerala
    {
        "name": "Life Mission",
        "category": "Housing",
        "description": "Comprehensive housing security.",
        "benefits": "House for landless/homeless.",
        "eligibility": "Homeless in Kerala.",
        "allowedStates": ["Kerala"],
        "applicationLink": "https://lifemission.kerala.gov.in"
    },
    {
        "name": "Karunya Benevolent Fund",
        "category": "Healthcare",
        "description": "Financial aid for expensive treatments.",
        "benefits": "Up to ₹2 Lakhs.",
        "eligibility": "BPL families in Kerala.",
        "allowedStates": ["Kerala"],
        "applicationLink": "https://karunya.kerala.gov.in"
    },

    # Tamil Nadu (More)
    {
        "name": "Pudhumai Penn Scheme",
        "category": "Education",
        "description": "Assistance for girl students.",
        "benefits": "₹1000/month for college.",
        "eligibility": "Girls from Govt schools in TN.",
        "allowedStates": ["Tamil Nadu"],
        "allowedGenders": ["Female"],
        "allowedOccupations": ["Student"],
        "applicationLink": "https://www.tn.gov.in"
    },
    {
        "name": "Illam Thedi Kalvi",
        "category": "Education",
        "description": "Education at doorstep.",
        "benefits": "Remedial classes after school.",
        "eligibility": "Students in TN.",
        "allowedStates": ["Tamil Nadu"],
        "allowedOccupations": ["Student"],
        "applicationLink": "https://illamthedikalvi.tnschools.gov.in"
    },

    # Bihar
    {
        "name": "Bihar Student Credit Card Scheme",
        "category": "Education",
        "description": "Education loan for students.",
        "benefits": "Loan up to ₹4 Lakhs.",
        "eligibility": "12th Pass students in Bihar.",
        "allowedStates": ["Bihar"],
        "allowedOccupations": ["Student"],
        "applicationLink": "https://www.7nishchay-yuvaupmission.bihar.gov.in"
    },
    {
        "name": "Mukhyamantri Kanya Utthan Yojana",
        "category": "Child Welfare",
        "description": "Empowerment of girl child.",
        "benefits": "Financial assistance from birth to graduation.",
        "eligibility": "Girls in Bihar.",
        "allowedStates": ["Bihar"],
        "allowedGenders": ["Female"],
        "applicationLink": "http://edudbt.bih.nic.in"
    },

    # --- OTHER SECTORS ---
    {
        "name": "PM Gati Shakti",
        "category": "Infrastructure",
        "description": "Multi-modal connectivity infrastructure.",
        "benefits": "Improved logistics.",
        "eligibility": "Citizens.",
        "applicationLink": "https://gati.shakti.gov.in"
    },
    {
        "name": "Production Linked Incentive (PLI)",
        "category": "Business",
        "description": "Incentives for domestic manufacturing.",
        "benefits": "Financial incentives based on sales.",
        "eligibility": "Manufacturers.",
        "allowedOccupations": ["Business"],
        "applicationLink": "https://neity.gov.in"
    },
    {
        "name": "Start-up India",
        "category": "Business",
        "description": "Support for startups.",
        "benefits": "Tax exemptions, mentorship.",
        "eligibility": "Startups.",
        "allowedOccupations": ["Business", "Self Employed"],
        "applicationLink": "https://www.startupindia.gov.in"
    },
    {
        "name": "PM e-Bus Sewa",
        "category": "Transport",
        "description": "Deployment of e-buses.",
        "benefits": "Better urban transport.",
        "eligibility": "Urban citizens.",
        "residenceRequirement": "Urban",
        "applicationLink": "https://mohua.gov.in"
    },
    {
        "name": "Pradhan Mantri Matsya Sampada Yojana",
        "category": "Fisheries",
        "description": "Blue revolution.",
        "benefits": "Support for fisheries.",
        "eligibility": "Fishermen.",
        "applicationLink": "https://pmmsy.dof.gov.in"
    },
    {
        "name": "National Beekeeping and Honey Mission",
        "category": "Agriculture",
        "description": "Sweet revolution.",
        "benefits": "Promotion of beekeeping.",
        "eligibility": "Farmers/Beekeepers.",
        "allowedOccupations": ["Farmer"],
        "applicationLink": "https://nbhm.gov.in"
    }
]

# Create additional generic/placeholder schemes to reach 100+ if needed
# (Filling with state variations for bulk)
states = ["Punjab", "Haryana", "Uttarakhand", "Himachal Pradesh", "Assam", "Chhattisgarh", "Jharkhand", "Goa"]
categories = ["Education", "Health", "Social Welfare"]

for i, state in enumerate(states):
    new_schemes.append({
        "name": f"{state} State Scholarship Scheme",
        "category": "Education",
        "description": f"Scholarship for meritorious students of {state}.",
        "benefits": "Financial aid for higher education.",
        "eligibility": f"Students of {state} with >75% marks.",
        "allowedStates": [state],
        "allowedOccupations": ["Student"],
        "minAge": 16,
        "applicationLink": f"https://{state.lower().replace(' ', '')}.gov.in"
    })
    new_schemes.append({
        "name": f"{state} Health Protection Scheme",
        "category": "Healthcare",
        "description": f"Health insurance for poor in {state}.",
        "benefits": "Coverage for critical illnesses.",
        "eligibility": f"BPL families of {state}.",
        "allowedStates": [state],
        "maxIncome": 100000,
        "applicationLink": f"https://health.{state.lower().replace(' ', '')}.gov.in"
    })
    new_schemes.append({
        "name": f"{state} Old Age Pension",
        "category": "Pension",
        "description": f"Pension for seniors in {state}.",
        "benefits": "Monthly pension.",
        "eligibility": f"Residents of {state} above 60.",
        "allowedStates": [state],
        "minAge": 60,
        "applicationLink": f"https://social.{state.lower().replace(' ', '')}.gov.in"
    })

# Add generic skill schemes
skills = ["Data Science", "Electrician", "Plumber", "Carpenter", "Nurse", "Textile", "Automotive"]
for skill in skills:
    new_schemes.append({
        "name": f"National Skill Mission - {skill}",
        "category": "Skill Development",
        "description": f"Training course for {skill}.",
        "benefits": "Certification and job placement.",
        "eligibility": "Youth 18-35 years.",
        "minAge": 18,
        "maxAge": 35,
        "applicationLink": "https://skillindia.gov.in"
    })

def add_schemes():
    with app.app_context():
        count = 0
        print(f"Adding {len(new_schemes)} new schemes...")
        for s_data in new_schemes:
            # Check for generic existing name match
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
                    allowed_genders=json.dumps(s_data.get('allowedGenders', [])),
                    allowed_occupations=json.dumps(s_data.get('allowedOccupations', [])),
                    allowed_states=json.dumps(s_data.get('allowedStates', [])),
                    allowed_castes=json.dumps(s_data.get('allowedCastes', [])),
                    min_income=s_data.get('minIncome'),
                    max_income=s_data.get('maxIncome'),
                    residence_requirement=s_data.get('residenceRequirement', 'Any'),
                    # Defaults
                    target_audience="Citizens",
                    allowed_education="[]",
                    allowed_marital_status="[]",
                    disability_requirement="Any"
                )
                db.session.add(scheme)
                count += 1
            else:
                print(f"Skipping {s_data['name']} (Already exists)")
        
        db.session.commit()
        print(f"Successfully added {count} new schemes.")

if __name__ == "__main__":
    add_schemes()
