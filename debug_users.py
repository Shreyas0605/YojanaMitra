from app import app, db, User, Admin, Scheme, PendingScheme, SchemeSource, AdminNotification, ScrapeLog
import json

with app.app_context():
    print("--- USER TABLE ---")
    for u in User.query.all():
        print(f"User {u.id}: {u.name} | {u.email}")
    
    print("\n--- ADMIN TABLE ---")
    for a in Admin.query.all():
        print(f"Admin {a.id}: {a.email}")

    print("\n--- SEARCHING ALL TABLES FOR 'Spoorthi' ---")
    # Just a broad search if possible, or check specific likely ones
    # Check if name is in any SchemeSource or something?
    # No, let's just grep the DB file if it's sqlite and small
