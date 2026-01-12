from app import app, db, Scheme
import json

def force_conflict():
    with app.app_context():
        # Get Schemes
        scheme_disability = Scheme.query.filter_by(name="Scholarships for Students with Disabilities").first()
        scheme_test = Scheme.query.filter_by(name="Detailed Test Scholarship Scheme").first()
        
        if not scheme_disability or not scheme_test:
            print("Schemes not found!")
            return

        print(f"Forcing conflict between: '{scheme_disability.name}' and '{scheme_test.name}'")

        # Set mutual exclusivity
        # For Disability Scheme
        disability_conflicts = json.loads(scheme_disability.mutually_exclusive_with) if scheme_disability.mutually_exclusive_with else []
        if str(scheme_test.id) not in disability_conflicts:
            disability_conflicts.append(str(scheme_test.id))
        
        scheme_disability.mutually_exclusive_with = json.dumps(disability_conflicts)

        # For Test Scheme
        test_conflicts = json.loads(scheme_test.mutually_exclusive_with) if scheme_test.mutually_exclusive_with else []
        if str(scheme_disability.id) not in test_conflicts:
            test_conflicts.append(str(scheme_disability.id))
            
        scheme_test.mutually_exclusive_with = json.dumps(test_conflicts)
        
        db.session.commit()
        print("✅ Conflict forced successfully.")

if __name__ == "__main__":
    force_conflict()
