from app import app, db, Admin
from werkzeug.security import generate_password_hash

def reset_admin():
    with app.app_context():
        # Create or Update Admin
        email = 'admin@yojanamitra.in'
        password = 'admin123'
        
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            admin.password_hash = generate_password_hash(password)
            print(f"Updated existing admin: {email}")
        else:
            admin = Admin(email=email, password_hash=generate_password_hash(password))
            db.session.add(admin)
            print(f"Created new admin: {email}")
        
        db.session.commit()
        print(f"Admin password set to: {password}")

if __name__ == "__main__":
    reset_admin()
