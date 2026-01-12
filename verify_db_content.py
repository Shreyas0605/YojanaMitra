from app import app, db, Scheme

with app.app_context():
    count = Scheme.query.count()
    print(f"Total Schemes in DB: {count}")
    
    if count > 0:
        first = Scheme.query.first()
        print(f"Sample Scheme: ID={first.id}, Name='{first.name}', Category='{first.category}'")
    else:
        print("Database is empty!")
