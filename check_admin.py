from app import app, db, Admin
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = Admin.query.filter_by(email='admin@yojanamitra.gov.in').first()
    if admin:
        print(f"Admin found: {admin.email}")
        # Reset password to be sure
        admin.password_hash = generate_password_hash('admin123')
        db.session.commit()
        print("Admin password reset to 'admin123'")
    else:
        print("Admin user NOT found. Creating...")
        new_admin = Admin(
            username='SuperAdmin',
            email='admin@yojanamitra.gov.in',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created successfully.")
