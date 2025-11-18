#!/usr/bin/env python3
"""
Diagnose why AI isn't working
"""

import sys
import os

print("=" * 70)
print("🔍 DIAGNOSING AI SETUP")
print("=" * 70)
print()

# Test 1: Check if library is installed
print("1️⃣  Checking google-generativeai library...")
try:
    import google.generativeai as genai
    print("   ✅ Library is installed")
except ImportError:
    print("   ❌ Library NOT installed!")
    print()
    print("   Install it with:")
    print("   pip install google-generativeai")
    print()
    sys.exit(1)

print()

# Test 2: Check environment file
print("2️⃣  Checking .env file...")
env_path = os.path.join('mcp_server', '.env')
if os.path.exists(env_path):
    print("   ✅ .env file exists")
    with open(env_path, 'r') as f:
        content = f.read()
        if 'GEMINI_API_KEY' in content:
            print("   ✅ GEMINI_API_KEY found in .env")
        else:
            print("   ❌ GEMINI_API_KEY NOT found in .env")
else:
    print("   ❌ .env file not found!")

print()

# Test 3: Load and test config
print("3️⃣  Testing configuration loading...")
sys.path.insert(0, 'mcp_server')
try:
    from dotenv import load_dotenv
    load_dotenv(env_path)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        # Remove quotes if present
        api_key = api_key.strip('"').strip("'")
        print(f"   ✅ API key loaded: {api_key[:20]}...")
        
        # Test API
        print()
        print("4️⃣  Testing Gemini API...")
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content("Say 'Working!' in one word.")
            print(f"   ✅ API Response: {response.text}")
            print()
            print("=" * 70)
            print("🎉 EVERYTHING IS WORKING!")
            print("=" * 70)
            print()
            print("If backend still shows static data:")
            print("1. Make sure you RESTARTED the backend after installing")
            print("2. Check backend terminal for '✅ Gemini AI enabled' messages")
            print("3. Try analyzing text with 100+ words")
            print()
        except Exception as e:
            print(f"   ❌ API test failed: {str(e)}")
            if "API_KEY_INVALID" in str(e):
                print("   💡 Your API key may be invalid")
    else:
        print("   ❌ API key not loaded from environment")
        
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print()
print("=" * 70)
