from app import app, db, UserDocument
import os

with app.app_context():
    print("Checking for new tables...")
    db.create_all()
    print("Done! UserDocument table is now ready.")
    
    # Create upload directory if missing
    upload_path = 'static/uploads/documents'
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        print(f"Created directory: {upload_path}")
