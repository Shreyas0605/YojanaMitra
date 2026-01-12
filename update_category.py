
import sys
import os
from app import app, db, Scheme

def update_cat():
    with app.app_context():
        s = Scheme.query.filter_by(name='Pradhan Mantri Jan Dhan Yojana (PMJDY)').first()
        if s:
            print(f"Old Category: {s.category}")
            s.category = 'Insurance' # Match PMJJBY
            db.session.commit()
            print(f"New Category: {s.category}")
        else:
            print("Scheme not found")

if __name__ == "__main__":
    sys.path.insert(0, os.getcwd())
    update_cat()
