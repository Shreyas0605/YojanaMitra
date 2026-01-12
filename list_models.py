import google.generativeai as genai
import os

GEMINI_API_KEY = "AIzaSyC9BQ_rJWTwLNgNUDJeP4FEsFY37ffPHiE"
genai.configure(api_key=GEMINI_API_KEY)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
