from app import app, db, Scheme
import json

def add_detailed_scheme():
    with app.app_context():
        # Check if already exists
        ext = Scheme.query.filter_by(name='Detailed Test Scholarship Scheme').first()
        if ext:
            db.session.delete(ext)
            db.session.commit()
            print("Deleted existing test scheme.")

        s = Scheme(
            name='Detailed Test Scholarship Scheme',
            description='A comprehensive scholarship scheme for students with disabilities pursuing higher education.',
            category='Education',
            target_audience='Students with Disabilities',
            benefits='• Maintenance Allowance: ₹1600/month (Hostellers), ₹750/month (Day Scholars)\n• Book Allowance: ₹1500/year\n• Disability Allowance: ₹2000-4000/year',
            eligibility='• Must be a student.\n• Pursuing Class 11th to Master\'s Degree.\n• Disability percentage 40% or above.\n• Family income < ₹2.5 Lakh/year.',
            exclusions='• Not for more than two students from a family.\n• Cannot hold any other scholarship.\n• False info leads to recovery with 15% interest.\n• No scholarship for repeat year.',
            application_process='1. Register at scholarships.gov.in\n2. Fill application form with ID and password.\n3. Upload documents.\n4. Final Submit.',
            documents_required='• Photograph\n• Proof of Age\n• Disability Certificate\n• Income Certificate\n• Tuition Fee Receipt.',
            min_age=16,
            max_age=35,
            allowed_genders=json.dumps(["Male", "Female", "Other"]),
            max_income=250000,
            allowed_states=json.dumps(["All"]),
            allowed_education=json.dumps(["12th Pass", "Graduate", "Post Graduate"]),
            disability_requirement='Yes',
            disability_percentage_min=40,
            application_link='https://scholarships.gov.in'
        )
        db.session.add(s)
        db.session.commit()
        print(f"Added scheme ID: {s.id}")

if __name__ == "__main__":
    add_detailed_scheme()
