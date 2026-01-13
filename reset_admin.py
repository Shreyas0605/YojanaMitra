from app import app, db, Admin
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = Admin.query.filter_by(email='admin@yojanamitra.gov.in').first()
    if admin:
        admin.password_hash = generate_password_hash('admin123')
        db.session.commit()
        print("✅ Admin password reset to 'admin123' for admin@yojanamitra.gov.in")
    else:
        new_admin = Admin(email='admin@yojanamitra.gov.in', password_hash=generate_password_hash('admin123'))
        db.session.add(new_admin)
        db.session.commit()
        print("✅ Created new Admin account: admin@yojanamitra.gov.in / admin123")
