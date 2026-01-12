
import sys
import os

# Add the application path
sys.path.insert(0, os.getcwd())

from app import app, db, Scheme

def reduce_schemes():
    with app.app_context():
        count = Scheme.query.count()
        print(f"Current scheme count: {count}")
        
        if count > 1000:
            limit = 1000
            # Get IDs to keep (first 1000)
            # We want to keep the "best" 1000? Or just the first 1000?
            # Let's just keep the first 1000 by ID for simplicity/stability
            
            # Fetch IDs of the first 1000 schemes
            # We'll use a subquery approach or just fetch all IDs and delete the rest
            # Since we deleting potentially thousands, let's just find the ID cutoff
            
            schemes = Scheme.query.order_by(Scheme.id).limit(1000).all()
            if not schemes:
                print("No schemes found to keep?")
                return

            last_id = schemes[-1].id
            print(f"Keeping schemes up to ID: {last_id}")
            
            # Delete schemes with ID > last_id
            deleted_count = Scheme.query.filter(Scheme.id > last_id).delete()
            db.session.commit()
            print(f"Deleted {deleted_count} schemes. New count should be <= 1000.")
            
            new_count = Scheme.query.count()
            print(f"New scheme count: {new_count}")
        else:
            print("Scheme count is already <= 1000. No action needed.")

if __name__ == "__main__":
    reduce_schemes()
