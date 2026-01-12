
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
print(f"Testing with API Key: {api_key[:10]}...")

genai.configure(api_key=api_key)

# Test both names
models_to_try = ['gemini-1.5-flash', 'gemini-flash-latest']

for model_name in models_to_try:
    print(f"\nTrying model: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"Success! Response: {response.text[:50]}...")
    except Exception as e:
        print(f"Failed: {e}")
