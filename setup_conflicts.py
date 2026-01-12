from app import app, db, Scheme
import json

def setup_conflicts():
    with app.app_context():
        # Scheme 42: Scholarships for Students with Disabilities
        # Scheme 19: Post Matric Scholarship for SC Students
        
        s42 = Scheme.query.get(42)
        s19 = Scheme.query.get(19)
        
        if s42 and s19:
            # Set mutual exclusivity
            s42.mutually_exclusive_with = json.dumps([19])
            s19.mutually_exclusive_with = json.dumps([42])
            
            db.session.commit()
            print(f"Set conflict between '{s42.name}' (42) and '{s19.name}' (19)")
        else:
            print("Schemes 42 or 19 not found.")

if __name__ == "__main__":
    setup_conflicts()
