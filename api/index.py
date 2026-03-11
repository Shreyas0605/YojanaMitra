from app import app, init_db

# Initialize DB and seed admin on cold start
with app.app_context():
    init_db()
