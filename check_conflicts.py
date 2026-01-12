
import sys
import os
import json

# Add the application path
sys.path.insert(0, os.getcwd())

from app import app, db, Scheme

def check_and_seed_conflicts():
    with app.app_context():
        # Check for existing conflicts
        schemes = Scheme.query.all()
        conflict_count = 0
        
        print("Checking for schemes with conflicts...")
        for s in schemes:
            if s.mutually_exclusive_with:
                try:
                    conflicts = json.loads(s.mutually_exclusive_with)
                    if conflicts:
                        print(f"Scheme '{s.name}' (ID: {s.id}) conflicts with: {conflicts}")
                        conflict_count += 1
                except:
                    pass
        
        print(f"Total schemes with conflicts: {conflict_count}")
        
        if conflict_count == 0:
            print("\nNo conflicts found! Seeding test data...")
            # Pick the first two schemes and make them mutually exclusive
            s1 = schemes[0]
            s2 = schemes[1]
            
            print(f"Making '{s1.name}' and '{s2.name}' mutually exclusive.")
            
            # Update s1
            s1.mutually_exclusive_with = json.dumps([str(s2.id)])
            
            # Update s2
            s2.mutually_exclusive_with = json.dumps([str(s1.id)])
            
            db.session.commit()
            print("Test conflicts added successfully.")
        else:
            print("\nConflicts already exist. You should be able to see them in the UI if valid.")

if __name__ == "__main__":
    check_and_seed_conflicts()
