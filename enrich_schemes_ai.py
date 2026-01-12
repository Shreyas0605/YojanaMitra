import os
import json
import time
from app import app, db, Scheme
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = 'gemini-flash-latest' # Changed from gemini-pro
model = genai.GenerativeModel(gemini_model)

ENRICH_PROMPT = """
You are a government scheme expert. I will give you a scheme name and description. 
Your task is to provide detailed, professional, and accurate information for the following sections:
1. Benefits (Bullet points)
2. Eligibility (Bullet points)
3. Exclusions (Bullet points)
4. Application Process (Numbered steps)
5. Documents Required (Bullet points)

Scheme Name: {name}
Brief Description: {description}

Return the response ONLY in valid JSON format with these keys:
"benefits", "eligibility", "exclusions", "application_process", "documents_required"

Example: {{
    "benefits": "• Point 1\\n• Point 2",
    "eligibility": "• Criteria 1\\n• Criteria 2",
    "exclusions": "• Not for...",
    "application_process": "1. Step one\\n2. Step two",
    "documents_required": "• Doc 1\\n• Doc 2"
}}
"""

def enrich_all():
    with app.app_context():
        schemes = Scheme.query.all()
        print(f"Total schemes to process: {len(schemes)}")
        
        for s in schemes:
            if s.benefits and len(s.benefits) > 100 and s.exclusions:
                print(f"Skipping '{s.name}' (already enriched)")
                continue
                
            print(f"Enriching '{s.name}'...")
            try:
                prompt = ENRICH_PROMPT.format(name=s.name, description=s.description)
                response = model.generate_content(prompt)
                
                # Cleanup potential markdown wrapper
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:-3].strip()
                elif text.startswith("```"):
                    text = text[3:-3].strip()
                    
                data = json.loads(text)
                
                s.benefits = data.get('benefits', s.benefits)
                s.eligibility = data.get('eligibility', s.eligibility)
                s.exclusions = data.get('exclusions', s.exclusions)
                s.application_process = data.get('application_process', s.application_process)
                s.documents_required = data.get('documents_required', s.documents_required)
                
                db.session.commit()
                print(f"Successfully enriched '{s.name}'")
                time.sleep(1) # Rate limit safety
                
            except Exception as e:
                print(f"Error enriching '{s.name}': {e}")
                db.session.rollback()

if __name__ == "__main__":
    enrich_all()
