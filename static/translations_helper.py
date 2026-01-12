# This Python script helps generate the enhanced index.html with full translations
# It will create a comprehensive HTML file with two-column layouts and Kannada translations

import os

# Paths for the generated illustrations
login_img = "C:/Users/91994/.gemini/antigravity/brain/32a51ef2-5daf-48d7-8ab1-ca4fa8fd589d/login_illustration_1764257512100.png"
register_img = "C:/Users/91994/.gemini/antigravity/brain/32a51ef2-5daf-48d7-8ab1-ca4fa8fd589d/register_illustration_1764257530659.png"
eligibility_img = "C:/Users/91994/.gemini/antigravity/brain/32a51ef2-5daf-48d7-8ab1-ca4fa8fd589d/eligibility_illustration_1764257625320.png"

# Kanna translations dictionary
translations = {
    # Navigation
    "Home": "ಮುಖಪುಟ",
    "Schemes": "ಯೋಜನೆಗಳು",
    "Check Eligibility": "ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ",
    "Login": "ಲಾಗಿನ್",
    "Register": "ನೋಂದಣಿ",
    "Profile": "ಪ್ರೊಫೈಲ್",
    "Logout": "ಲಾಗ್ಔಟ್",
    "Admin Panel": "ನಿರ್ವಾಹಕ ಪ್ಯಾನೆಲ್",
    
    # Common
    "Submit": "ಸಲ್ಲಿಸಿ",
    "Cancel": "ರದ್ದುಮಾಡಿ",
    "Save": "ಉಳಿಸಿ",
    "Search": "ಹುಡುಕಿ",
    "Apply Now": "ಈಗ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ",
    
    # Login Page
    "Welcome Back!": "ಮರಳಿ ಸ್ವಾಗತ!",
    "Access Your Personalized Welfare Dashboard": "ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಕಲ್ಯಾಣ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಪ್ರವೇಶಿಸಿ",
    "Secure Login": "ಸುರಕ್ಷಿತ ಲಾಗಿನ್",
    "Login to Your Account": "ನಿಮ್ಮ ಖಾತೆಗೆ ಲಾಗಿನ್ ಆಗಿ",
    "Email": "ಇಮೇಲ್",
    "Password": "ಪಾಸ್ವರ್ಡ್",
    "Enter your email": "ನಿಮ್ಮ ಇಮೇಲ್ ನಮೂದಿಸಿ",
    "Enter your password": "ನಿಮ್ಮ ಪಾಸ್ವರ್ಡ್ ನಮೂದಿಸಿ",
    "Don't have an account?": "ಖಾತೆ ಇಲ್ಲವೇ?",
    
    # Register Page
    "Join YojanaMitra": "ಯೋಜನಾಮಿತ್ರಕ್ಕೆ ಸೇರಿ",
    "Start Your Journey to Government Benefits": "ಸರ್ಕಾರಿ ಪ್ರಯೋಜನಗಳ ಕಡೆಗೆ ನಿಮ್ಮ ಪ್ರಯಾಣ ಪ್ರಾರಂಭಿಸಿ",
    "Create Account": "ಖಾತೆ ತೆರೆಯಿರಿ",
    "Create Your Account": "ನಿಮ್ಮ ಖಾತೆ ತೆರೆಯಿರಿ",
    "Full Name": "ಪೂರ್ಣ ಹೆಸರು",
    "Mobile": "ಮೊಬೈಲ್",
    "Enter your full name": "ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರು ನಮೂದಿಸಿ",
    "Enter your mobile number": "ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ",
    "Already have an account?": "ಈಗಾಗಲೇ ಖಾತೆ ಇದೆಯೇ?",
    
    # Eligibility Page  
    "Find Your Perfect Schemes": "ನಿಮಗೆ ಸೂಕ್ತ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
    "AI-Powered Matching for Maximum Benefits": "ಗರಿಷ್ಠ ಪ್ರಯೋಜನಕ್ಕಾಗಿ AI-ಚಾಲಿತ ಹೊಂದಾಣಿಕೆ",
    "Check Your Eligibility": "ನಿಮ್ಮ ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ",
    "Enter Your Details": "ನಿಮ್ಮ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ",
    "Age": "ವಯಸ್ಸು",
    "Gender": "ಲಿಂಗ",
    "State": "ರಾಜ್ಯ",
    "Occupation": "ಉದ್ಯೋಗ",
    "Annual Income": "ವಾರ್ಷಿಕ ಆದಾಯ",
    "Caste": "ಜಾತಿ",
    "Find Schemes": "ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ",
    "Enter your age": "ನಿಮ್ಮ ವಯಸ್ಸು ನಮೂದಿಸಿ",
    "Select gender": "ಲಿಂಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    "Enter your state": "ನಿಮ್ಮ ರಾಜ್ಯವನ್ನು ನಮೂದಿಸಿ",
    "Enter your occupation": "ನಿಮ್ಮ ಉದ್ಯೋಗವನ್ನು ನಮೂದಿಸಿ",
    "Enter annual income": "ವಾರ್ಷಿಕ ಆದಾಯವನ್ನು ನಮೂದಿಸಿ",
    "Male": "ಪುರುಷ",
    "Female": "ಮಹಿಳೆ",
    "Other": "ಇತರೆ",
    "Select": "ಆಯ್ಕೆಮಾಡಿ",
    
    # Home Page
    "YojanaMitra": "ಯೋಜನಾಮಿತ್ರ",
    "Government Welfare Made Simple": "ಸರ್ಕಾರಿ ಕಲ್ಯಾಣ ಸರಳಗೊಳಿಸಲಾಗಿದೆ",
    "Discover 50+ government schemes": "50+ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ",
    "Browse Schemes": "ಯೋಜನೆಗಳನ್ನು ವೀಕ್ಷಿಸಿ",
    "How It Works": "ಇದು ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ",
    "Popular Categories": "ಜನಪ್ರಿಯ ವರ್ಗಗಳು",
}

print("Translation dictionary created successfully!")
print(f"Total translations: {len(translations)}")
