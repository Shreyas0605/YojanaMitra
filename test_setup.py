from app import app, db, Scheme
with app.app_context():
    s = Scheme(
        name='Special Artisan Support', 
        description='For weavers and handloom workers', 
        category='Economic', 
        allowed_states='["All"]', 
        allowed_genders='["All"]'
    )
    db.session.add(s)
    db.session.commit()
    print(f'Created Scheme ID: {s.id}')
