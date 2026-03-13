import google.generativeai as genai
import os
import json
from app import app, db, Scheme

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

def enrich_poshan():
    with app.app_context():
        scheme = Scheme.query.filter_by(name='Poshan Abhiyaan').first()
        if not scheme:
            print("Poshan Abhiyaan not found!")
            return

        print(f"Enriching: {scheme.name}...")
        prompt = f"""
        You are an expert government welfare consultant. I need detailed information for the scheme: "{scheme.name}".
        Category: {scheme.category}
        Current Description: {scheme.description}

        Please generate detailed, point-wise content for the following fields. 
        Format your response as a valid JSON object with these exact keys:
        - "benefits": A bulleted list (str) of 3-5 key benefits. Use '•' as bullet.
        - "eligibility": A bulleted list (str) of 3-5 specific eligibility criteria. Use '•' as bullet.
        - "repl_exclusions": A bulleted list (str) of 3-5 common exclusions/disqualifications. Use '•' as bullet.
        - "application_process": A numbered list (str) of 3-5 steps to apply.
        - "documents_required": A bulleted list (str) of 3-5 required documents. Use '•' as bullet.

        IMPORTANT: Return ONLY the raw JSON string.
        """

        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]
                
            data = json.loads(text)
            
            scheme.benefits = data.get("benefits", scheme.benefits)
            scheme.eligibility = data.get("eligibility", scheme.eligibility)
            
            criteria = scheme.get_criteria()
            criteria['exclusions'] = data.get("repl_exclusions", "None")
            criteria['applicationProcess'] = data.get("application_process", "Check official portal.")
            criteria['documentsRequired'] = data.get("documents_required", "Aadhaar Card")
            
            scheme.criteria = json.dumps(criteria)
            db.session.commit()
            print(f"[SUCCESS] Enriched Poshan Abhiyaan")
            print(f"Benefits: {scheme.benefits}")
            
        except Exception as e:
            print(f"[FAILED] {e}")

if __name__ == "__main__":
    enrich_poshan()
