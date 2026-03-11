from app import app, db

# Initialize DB tables on cold start (runs once per serverless instance)
with app.app_context():
    db.create_all()
