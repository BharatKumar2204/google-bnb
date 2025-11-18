#!/usr/bin/env python3
"""
Test if text analysis is using Gemini
"""

import requests
import json

print("=" * 70)
print("🧪 TESTING TEXT ANALYSIS WITH GEMINI")
print("=" * 70)
print()

# Test 1: High credibility text
print("Test 1: High Credibility Text")
print("-" * 70)

text1 = """According to a peer-reviewed study published in Nature journal by MIT researchers, 
a new renewable energy breakthrough has been achieved with 95% efficiency improvements. 
The research was conducted over 3 years and peer-reviewed by leading scientists."""

print(f"Text: {text1[:100]}...")
print()

try:
    response = requests.post(
        "http://localhost:8000/agents/truth_verification",
        json={"text": text1, "article_id": "test1"},
        timeout=60  # Increased to 60 seconds for Gemini analysis
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Response received")
        print(f"   Full response: {json.dumps(data, indent=2)}")
        
        result = data.get('data', {})
        print(f"   Score: {result.get('score', 'N/A')}/100")
        print(f"   Verdict: {result.get('verdict', 'N/A')}")
        print(f"   Method: {result.get('method', 'unknown')}")
        
        if result.get('method') == 'ai_powered':
            print("   🤖 Using AI!")
        else:
            print("   📊 Using rule-based")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print()
    print("Make sure backend is running:")
    print("  cd mcp_server && python run_server.py")

print()
print("=" * 70)

# Test 2: Low credibility text
print("Test 2: Low Credibility Text")
print("-" * 70)

text2 = "You won't believe this miracle cure! Doctors hate this one trick!"

print(f"Text: {text2}")
print()

try:
    response = requests.post(
        "http://localhost:8000/agents/truth_verification",
        json={"text": text2, "article_id": "test2"},
        timeout=60  # Increased to 60 seconds for Gemini analysis
    )
    
    if response.status_code == 200:
        data = response.json()
        result = data.get('data', {})
        
        print(f"✅ Response received")
        print(f"   Score: {result.get('score', 'N/A')}/100")
        print(f"   Verdict: {result.get('verdict', 'N/A')}")
        print(f"   Method: {result.get('method', 'unknown')}")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")

print()
print("=" * 70)
print("📊 ANALYSIS")
print("=" * 70)
print()
print("If scores are different (not both 50), Gemini is working!")
print("If method shows 'ai_powered', Gemini is being used!")
print()
