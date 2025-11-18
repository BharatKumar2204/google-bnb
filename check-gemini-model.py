#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv('mcp_server/.env')

api_key = os.getenv('GEMINI_API_KEY', '').strip('"').strip("'")
genai.configure(api_key=api_key)

print("Testing Gemini models...")
print()

# Test gemini-2.5-pro
print("1. Testing gemini-2.5-pro:")
try:
    model = genai.GenerativeModel('gemini-2.5-pro')
    response = model.generate_content("Say 'Working!' in one word.")
    print(f"   ✅ Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    print()
    print("2. Testing gemini-2.0-flash-exp instead:")
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Say 'Working!' in one word.")
        print(f"   ✅ Response: {response.text}")
        print()
        print("   💡 Use 'gemini-2.0-flash-exp' instead of 'gemini-2.5-pro'")
    except Exception as e2:
        print(f"   ❌ Error: {str(e2)}")

print()
print("Available models:")
for m in genai.list_models():
    if 'gemini' in m.name.lower():
        print(f"   - {m.name}")
