from app import app, db, User

def check_recipients():
    with app.app_context():
        users = User.query.all()
        print(f"Total Users: {len(users)}")
        print("-" * 60)
        print(f"{'ID':<5} {'Name':<20} {'Mobile':<15} {'Email'}")
        print("-" * 60)
        
        for user in users:
            email = user.email if user.email else "(No Email)"
            mobile = user.mobile if user.mobile else "(No Mobile)"
            print(f"{user.id:<5} {user.name:<20} {mobile:<15} {email}")
            
if __name__ == "__main__":
    check_recipients()
