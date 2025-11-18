#!/usr/bin/env python3
"""
Test if Gemini API is working
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv('mcp_server/.env')

print("=" * 70)
print("🧪 TESTING GEMINI API")
print("=" * 70)
print()

# Check API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"1️⃣  API Key found: {'✅ Yes' if api_key else '❌ No'}")
if api_key:
    print(f"   Key starts with: {api_key[:20]}...")
print()

# Try to import library
print("2️⃣  Testing google-generativeai library...")
try:
    import google.generativeai as genai
    print("   ✅ Library imported successfully")
except ImportError as e:
    print(f"   ❌ Library not installed: {e}")
    print()
    print("   Install it with:")
    print("   pip install google-generativeai")
    exit(1)
print()

# Try to configure
print("3️⃣  Configuring Gemini...")
try:
    genai.configure(api_key=api_key)
    print("   ✅ Configuration successful")
except Exception as e:
    print(f"   ❌ Configuration failed: {e}")
    exit(1)
print()

# Try to create model
print("4️⃣  Creating model...")
try:
    model = genai.GenerativeModel('gemini-pro')
    print("   ✅ Model created successfully")
except Exception as e:
    print(f"   ❌ Model creation failed: {e}")
    exit(1)
print()

# Try to generate content
print("5️⃣  Testing content generation...")
try:
    response = model.generate_content("Say 'Hello, I am working!' in one sentence.")
    print(f"   ✅ Response: {response.text}")
except Exception as e:
    print(f"   ❌ Generation failed: {e}")
    print()
    if "API_KEY_INVALID" in str(e):
        print("   💡 Your API key appears to be invalid")
        print("   Check: https://makersuite.google.com/app/apikey")
    exit(1)
print()

print("=" * 70)
print("🎉 SUCCESS! Gemini API is working correctly!")
print("=" * 70)
print()
print("Your verification agent should now use AI-powered analysis.")
print("Restart your backend to apply changes.")
