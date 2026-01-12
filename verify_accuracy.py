from app import app, db, Scheme, User, calculate_match_score
import json

class TempUser:
    def __init__(self, data):
        self.age = data.get('age', 25)
        self.gender = data.get('gender', 'Male')
        self.occupation = data.get('occupation', 'Student')
        self.income = data.get('income', 50000)
        self.caste = data.get('caste', 'General')
        self.state = data.get('state', 'Karnataka')
        self.education = data.get('education', 'Graduate')
        self.marital_status = data.get('marital_status', 'Single')
        self.disability = data.get('disability', 'No')
        self.residence = data.get('residence', 'Urban')
        self.father_occupation = data.get('father_occupation', 'Farmer')
        self.mother_occupation = data.get('mother_occupation', 'Homemaker')
        self.religion = data.get('religion', 'Hindu')
        self.land_type = data.get('land_type', 'None')
        self.is_orphan = data.get('is_orphan', 'No')
        self.is_tribal = data.get('is_tribal', 'No')
        self.is_farmer = 'No'
        self.minority_status = 'No'
        self.is_widow_single_woman = 'No'
        self.is_senior_citizen = 'No'

with app.app_context():
    scheme = Scheme.query.get(57)
    print(f"Testing Scheme: {scheme.name}")
    
    # Test case 1: Non-Artisan
    user1 = TempUser({
        'occupation': 'Student',
        'father_occupation': 'Farmer'
    })
    score1 = calculate_match_score(user1, scheme)
    print(f"Test 1 (Non-Artisan): Match Score = {score1}% (Expected: 0%)")
    
    # Test case 2: Artisan Himself
    user2 = TempUser({
        'occupation': 'Artisan'
    })
    score2 = calculate_match_score(user2, scheme)
    # Note: Artisan needs to be in allowed_occupations for the basic guard to pass too, 
    # but the test scheme has no occupations set (None), so basic guard passes.
    print(f"Test 2 (User is Artisan): Match Score = {score2}% (Expected: >0%)")

    # Test case 3: Child of Weaver
    user3 = TempUser({
        'occupation': 'Student',
        'father_occupation': 'Weaver'
    })
    score3 = calculate_match_score(user3, scheme)
    print(f"Test 3 (Child of Weaver): Match Score = {score3}% (Expected: >0%)")
