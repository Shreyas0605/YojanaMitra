from app import app, db, init_db

def reinit():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        print("Seeding database...")
        init_db()
        print("Database re-initialized successfully.")

if __name__ == "__main__":
    reinit()
