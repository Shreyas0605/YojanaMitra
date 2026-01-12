import sys
import os
import json

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Scheme

def create_test_scheme():
    with app.app_context():
        # Clean up old test schemes
        Scheme.query.filter_by(name="Detailed Test Scholarship Scheme").delete()
        
        test_scheme = Scheme(
            name="Detailed Test Scholarship Scheme",
            description="A comprehensive scholarship scheme for students with disabilities pursuing higher education.",
            category="Education",
            benefits="Maintenance Allowance: ₹1600/month (Hostellers), ₹750/month (Day Scholars)\nBook Allowance: ₹1500/year\nDisability Allowance: ₹2000-4000/year",
            eligibility="1. Must be a student.\n2. Pursuing Class 11th to Master's Degree.\n3. Disability percentage 40% or above.\n4. Family income < ₹2.5 Lakh/year.",
            application_link="https://scholarships.gov.in/",
            exclusions="1. Not for more than two students from a family.\n2. Cannot hold any other scholarship.\n3. False info leads to recovery with 15% interest.\n4. No scholarship for repeat year.",
            application_process="Step 1: Register at scholarships.gov.in\nStep 2: Fill application form with ID and password.\nStep 3: Upload documents.\nStep 4: Final Submit.",
            documents_required="1. Photograph\n2. Proof of Age\n3. Disability Certificate\n4. Income Certificate\n5. Tuition Fee Receipt",
            allowed_genders=json.dumps(["Male", "Female", "Other"]),
            min_age=15,
            max_age=35,
            allowed_states=json.dumps(["All"]),
            allowed_castes=json.dumps(["All"])
        )
        
        db.session.add(test_scheme)
        db.session.commit()
        print(f"Test scheme created with ID: {test_scheme.id}")

if __name__ == "__main__":
    create_test_scheme()
