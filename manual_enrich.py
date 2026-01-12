from app import app, db, Scheme
import json

def manual_enrich():
    with app.app_context():
        scheme = Scheme.query.filter_by(name='Poshan Abhiyaan').first()
        if not scheme:
            print("Scheme not found")
            return

        print(f"Manually enriching {scheme.name}...")
        
        # Hardcoded researched data
        scheme.benefits = json.dumps([
            "Reduced stunting in children (0-6 years) by 2% per annum.",
            "Reduced under-nutrition (underweight) by 2% per annum.",
            "Reduction in anemia among young children, women and adolescent girls by 3% per annum.",
            "Low Birth Weight (LBW) reduction by 2% per annum.",
            "Access to Anganwadi Services and nutritional support."
        ])
        
        scheme.eligibility = json.dumps([
            "Children in the age group of 0-6 years.",
            "Pregnant Women and Lactating Mothers (PW&LM).",
            "Adolescent Girls in the age group of 14-18 years in Aspirational Districts.",
            "Must be registered at the nearest Anganwadi Centre.",
            "Must have an Aadhaar card (for tracking)."
        ])
        
        # Update columns directly
        print(f"Updating columns...")
        scheme.exclusions = json.dumps([
            "Families above the poverty line (in some specific sub-schemes).",
            "Beneficiaries already receiving similar supplementary nutrition from other central schemes."
        ])
        scheme.application_process = json.dumps([
            "Visit your nearest Anganwadi Centre (AWC).",
            "Register with the Anganwadi Worker (AWW) using Aadhaar and MCP card.",
            "Regularly attend health check-ups and growth monitoring sessions.",
            "Receive Take Home Ration (THR) or Hot Cooked Meal (HCM) as per entitlement."
        ])
        scheme.documents_required = json.dumps([
            "Aadhaar Card of Child and Mother/Guardian",
            "Mother Copy of MCP Card",
            "Bank Account Details (for cash transfers if applicable)",
            "Residential Proof"
        ])
        
        db.session.commit()
        print("✅ Successfully updated Poshan Abhiyaan with manual data.")

if __name__ == "__main__":
    manual_enrich()
