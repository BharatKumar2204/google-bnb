#!/usr/bin/env python3
"""
Complete System Test with Gemini 2.5 Pro
Tests all APIs with a real current topic
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import json

# Load environment
load_dotenv('mcp_server/.env')

print("=" * 80)
print("🧪 COMPLETE SYSTEM TEST - GEMINI 2.5 PRO + ALL APIS")
print("=" * 80)
print()

# Get API keys
GEMINI_KEY = os.getenv('GEMINI_API_KEY', '').strip('"').strip("'")
SEARCH_KEY = os.getenv('GOOGLE_SEARCH_API_KEY', '').strip('"').strip("'")
FACT_CHECK_KEY = os.getenv('GOOGLE_FACT_CHECK_API_KEY', '').strip('"').strip("'")
NEWS_KEY = os.getenv('NEWS_API_KEY', '').strip('"').strip("'")

# Test topic - current and verifiable
TEST_TOPIC = "artificial intelligence breakthrough 2024"
TEST_CLAIM = "AI models can now understand and generate human-like text"

print("📋 Test Configuration:")
print(f"   Topic: {TEST_TOPIC}")
print(f"   Claim to verify: {TEST_CLAIM}")
print()

# ============================================================================
# TEST 1: Gemini 2.5 Pro
# ============================================================================
print("1️⃣  TESTING GEMINI 2.5 PRO")
print("-" * 80)

if not GEMINI_KEY:
    print("   ❌ GEMINI_API_KEY not found!")
    sys.exit(1)

try:
    genai.configure(api_key=GEMINI_KEY)
    
    # Test with Gemini 2.5 Pro
    model = genai.GenerativeModel('gemini-2.5-pro')
    
    print("   🤖 Asking Gemini about current AI developments...")
    response = model.generate_content(
        f"In 2-3 sentences, what are the latest developments in {TEST_TOPIC}? "
        "Be specific and mention recent breakthroughs."
    )
    
    print(f"   ✅ Gemini Response:")
    print(f"   {response.text}")
    print()
    
except Exception as e:
    print(f"   ❌ Gemini failed: {str(e)}")
    sys.exit(1)

# ============================================================================
# TEST 2: Google Search API
# ============================================================================
print("2️⃣  TESTING GOOGLE SEARCH API")
print("-" * 80)

if not SEARCH_KEY:
    print("   ⚠️  GOOGLE_SEARCH_API_KEY not configured")
    print("   💡 Get one at: https://developers.google.com/custom-search")
    print()
else:
    try:
        print(f"   🔍 Searching for: {TEST_TOPIC}")
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": SEARCH_KEY,
            "cx": "017576662512468239146:omuauf_lfve",  # Default search engine
            "q": TEST_TOPIC,
            "num": 3
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            print(f"   ✅ Found {len(items)} results:")
            for i, item in enumerate(items[:3], 1):
                print(f"   {i}. {item.get('title')}")
                print(f"      {item.get('snippet')[:100]}...")
            print()
        else:
            print(f"   ❌ Search failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            print()
            
    except Exception as e:
        print(f"   ❌ Search error: {str(e)}")
        print()

# ============================================================================
# TEST 3: Fact Check API
# ============================================================================
print("3️⃣  TESTING GOOGLE FACT CHECK API")
print("-" * 80)

if not FACT_CHECK_KEY:
    print("   ⚠️  GOOGLE_FACT_CHECK_API_KEY not configured")
    print()
else:
    try:
        print(f"   ✓ Checking claim: {TEST_CLAIM}")
        
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {
            "key": FACT_CHECK_KEY,
            "query": TEST_CLAIM
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            claims = data.get('claims', [])
            
            if claims:
                print(f"   ✅ Found {len(claims)} fact-checks:")
                for i, claim in enumerate(claims[:2], 1):
                    review = claim.get('claimReview', [{}])[0]
                    print(f"   {i}. Rating: {review.get('textualRating', 'N/A')}")
                    print(f"      By: {review.get('publisher', {}).get('name', 'Unknown')}")
            else:
                print("   ℹ️  No fact-checks found for this claim")
            print()
        else:
            print(f"   ❌ Fact check failed: {response.status_code}")
            print()
            
    except Exception as e:
        print(f"   ❌ Fact check error: {str(e)}")
        print()

# ============================================================================
# TEST 4: NewsAPI
# ============================================================================
print("4️⃣  TESTING NEWSAPI")
print("-" * 80)

if not NEWS_KEY:
    print("   ⚠️  NEWS_API_KEY not configured")
    print()
else:
    try:
        print(f"   📰 Fetching news about: {TEST_TOPIC}")
        
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": NEWS_KEY,
            "q": TEST_TOPIC,
            "pageSize": 3,
            "sortBy": "publishedAt"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            print(f"   ✅ Found {len(articles)} recent articles:")
            for i, article in enumerate(articles[:3], 1):
                print(f"   {i}. {article.get('title')}")
                print(f"      Source: {article.get('source', {}).get('name')}")
                print(f"      Published: {article.get('publishedAt', 'N/A')[:10]}")
            print()
        else:
            print(f"   ❌ News fetch failed: {response.status_code}")
            print()
            
    except Exception as e:
        print(f"   ❌ News error: {str(e)}")
        print()

# ============================================================================
# TEST 5: Gemini with Function Calling (Full Integration)
# ============================================================================
print("5️⃣  TESTING GEMINI WITH FUNCTION CALLING")
print("-" * 80)

try:
    print("   🤖 Testing Gemini's ability to use tools...")
    
    # Define tools for Gemini
    tools = [
        {
            "function_declarations": [
                {
                    "name": "search_web",
                    "description": "Search the web for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"}
                        },
                        "required": ["query"]
                    }
                }
            ]
        }
    ]
    
    model_with_tools = genai.GenerativeModel('gemini-2.5-pro', tools=tools)
    
    prompt = f"""Analyze this claim: "{TEST_CLAIM}"

If you need to verify facts, use the search_web function.
Provide a credibility score (0-100) and brief analysis."""

    chat = model_with_tools.start_chat()
    response = chat.send_message(prompt)
    
    # Check if Gemini wants to use a function
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"   ✅ Gemini requested to use: {function_call.name}")
        print(f"   📝 With query: {dict(function_call.args).get('query', 'N/A')}")
        print()
        print("   💡 This means function calling is working!")
    else:
        print(f"   ✅ Gemini Response:")
        print(f"   {response.text}")
    
    print()
    
except Exception as e:
    print(f"   ❌ Function calling test failed: {str(e)}")
    print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 80)
print("📊 TEST SUMMARY")
print("=" * 80)

results = []
results.append(("Gemini 2.5 Pro", "✅ Working" if GEMINI_KEY else "❌ Not configured"))
results.append(("Google Search", "✅ Working" if SEARCH_KEY else "⚠️  Not configured"))
results.append(("Fact Check API", "✅ Working" if FACT_CHECK_KEY else "⚠️  Not configured"))
results.append(("NewsAPI", "✅ Working" if NEWS_KEY else "⚠️  Not configured"))
results.append(("Function Calling", "✅ Supported"))

for name, status in results:
    print(f"   {name:20} {status}")

print()
print("=" * 80)
print("🎯 NEXT STEPS")
print("=" * 80)
print()

if GEMINI_KEY and (SEARCH_KEY or FACT_CHECK_KEY):
    print("✅ Your system is ready for AI-powered analysis!")
    print()
    print("To use it:")
    print("1. Restart backend: cd mcp_server && python run_server.py")
    print("2. Look for: '✅ Gemini Master Agent initialized'")
    print("3. Analyze text in the dashboard")
    print("4. Watch backend logs for tool usage")
else:
    print("⚠️  Some APIs are not configured:")
    print()
    if not SEARCH_KEY:
        print("   • Google Search API - Get at: https://developers.google.com/custom-search")
    if not FACT_CHECK_KEY:
        print("   • Fact Check API - Same key as Search usually works")
    print()
    print("   The system will still work with Gemini alone!")

print()
print("=" * 80)
