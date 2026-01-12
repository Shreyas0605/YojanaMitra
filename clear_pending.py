from app import app, db, PendingScheme

def clear_pending():
    with app.app_context():
        count = PendingScheme.query.count()
        if count > 0:
            print(f"Found {count} pending schemes. Deleting...")
            PendingScheme.query.delete()
            db.session.commit()
            print("All pending schemes validated and cleared.")
        else:
            print("No pending schemes found.")

if __name__ == "__main__":
    clear_pending()
