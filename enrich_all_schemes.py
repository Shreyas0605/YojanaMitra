import google.generativeai as genai
import os
import json
import time
from app import app, db, Scheme

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

def enrich_scheme(scheme):
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

    Keep the tone professional, clear, and encouraging.
    If exact details are unknown, infer reasonably based on standard Indian government schemes for this category.
    IMPORTANT: Return ONLY the raw JSON string, no markdown formatting.
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean potential markdown code blocks
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
            
        data = json.loads(text)
        
        # Update Scheme (using set attributes to ensure we trigger updates)
        scheme.benefits = data.get("benefits", scheme.benefits)
        scheme.eligibility = data.get("eligibility", scheme.eligibility)
        
        # Parse Criteria JSON to update nested fields
        criteria = scheme.get_criteria()
        criteria['exclusions'] = data.get("repl_exclusions", "None")
        criteria['applicationProcess'] = data.get("application_process", "Check official portal.")
        criteria['documentsRequired'] = data.get("documents_required", "Aadhaar Card, Income Certificate")
        
        scheme.criteria = json.dumps(criteria)
        
        db.session.commit()
        print(f"[SUCCESS] Updated {scheme.name}")
        
    except Exception as e:
        print(f"[FAILED] to enrich {scheme.name}: {e}")

def main():
    with app.app_context():
        schemes = Scheme.query.all()
        print(f"Found {len(schemes)} schemes. Starting enrichment...")
        
        for scheme in schemes:
            enrich_scheme(scheme)
            time.sleep(1.5) # Rate limit protection

if __name__ == "__main__":
    main()
