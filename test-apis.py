#!/usr/bin/env python3
"""
Test script to verify all API keys are working
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), 'mcp_server', '.env')
load_dotenv(env_path)

print("=" * 70)
print("🔑 API KEY VERIFICATION TEST")
print("=" * 70)
print()

# Test results
results = []

# 1. Test NewsAPI
print("1️⃣  Testing NewsAPI...")
news_api_key = os.getenv("NEWS_API_KEY")
if news_api_key:
    try:
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "ok":
                print("   ✅ NewsAPI: Working!")
                print(f"   📰 Found {data.get('totalResults', 0)} articles")
                results.append(("NewsAPI", True))
            else:
                print(f"   ❌ NewsAPI: Error - {data.get('message', 'Unknown error')}")
                results.append(("NewsAPI", False))
        else:
            print(f"   ❌ NewsAPI: HTTP {response.status_code}")
            results.append(("NewsAPI", False))
    except Exception as e:
        print(f"   ❌ NewsAPI: {str(e)}")
        results.append(("NewsAPI", False))
else:
    print("   ⚠️  NewsAPI: Key not found")
    results.append(("NewsAPI", None))

print()

# 2. Test Google Gemini API
print("2️⃣  Testing Google Gemini API...")
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    try:
        # Test with a simple API call
        response = requests.get(
            f"https://generativelanguage.googleapis.com/v1/models?key={gemini_key}",
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Gemini API: Working!")
            results.append(("Gemini API", True))
        else:
            print(f"   ❌ Gemini API: HTTP {response.status_code}")
            results.append(("Gemini API", False))
    except Exception as e:
        print(f"   ❌ Gemini API: {str(e)}")
        results.append(("Gemini API", False))
else:
    print("   ⚠️  Gemini API: Key not found")
    results.append(("Gemini API", None))

print()

# 3. Test Google Fact Check API
print("3️⃣  Testing Google Fact Check API...")
fact_check_key = os.getenv("GOOGLE_FACT_CHECK_API_KEY")
if fact_check_key:
    try:
        response = requests.get(
            f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query=test&key={fact_check_key}",
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Fact Check API: Working!")
            results.append(("Fact Check API", True))
        else:
            print(f"   ❌ Fact Check API: HTTP {response.status_code}")
            results.append(("Fact Check API", False))
    except Exception as e:
        print(f"   ❌ Fact Check API: {str(e)}")
        results.append(("Fact Check API", False))
else:
    print("   ⚠️  Fact Check API: Key not found")
    results.append(("Fact Check API", None))

print()

# 4. Test Google Cloud Credentials
print("4️⃣  Testing Google Cloud Credentials...")
creds_path = os.path.join(os.path.dirname(__file__), 'mcp_server', 'credentials.json')
if os.path.exists(creds_path):
    try:
        import json
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        
        if creds.get("type") == "service_account":
            print("   ✅ Credentials file: Valid format")
            print(f"   📧 Service account: {creds.get('client_email')}")
            print(f"   🆔 Project ID: {creds.get('project_id')}")
            results.append(("GCP Credentials", True))
        else:
            print("   ❌ Credentials file: Invalid format")
            results.append(("GCP Credentials", False))
    except Exception as e:
        print(f"   ❌ Credentials file: {str(e)}")
        results.append(("GCP Credentials", False))
else:
    print("   ⚠️  Credentials file: Not found")
    results.append(("GCP Credentials", None))

print()

# 5. Test Twitter API (Optional)
print("5️⃣  Testing Twitter API (Optional)...")
twitter_token = os.getenv("TWITTER_BEARER_TOKEN")
if twitter_token:
    try:
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/recent?query=test&max_results=10",
            headers={"Authorization": f"Bearer {twitter_token}"},
            timeout=10
        )
        if response.status_code == 200:
            print("   ✅ Twitter API: Working!")
            results.append(("Twitter API", True))
        else:
            print(f"   ⚠️  Twitter API: HTTP {response.status_code} (May need elevated access)")
            results.append(("Twitter API", None))
    except Exception as e:
        print(f"   ❌ Twitter API: {str(e)}")
        results.append(("Twitter API", False))
else:
    print("   ⚠️  Twitter API: Key not found (Optional)")
    results.append(("Twitter API", None))

print()
print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)

working = sum(1 for _, status in results if status is True)
failed = sum(1 for _, status in results if status is False)
missing = sum(1 for _, status in results if status is None)

print(f"✅ Working: {working}")
print(f"❌ Failed: {failed}")
print(f"⚠️  Missing/Optional: {missing}")
print()

if working >= 2:
    print("🎉 Great! You have enough APIs configured to run the app!")
    print()
    print("Next steps:")
    print("1. Run: start-backend.bat")
    print("2. Run: start-frontend.bat (in another terminal)")
    print("3. Open: http://localhost:3000")
elif working >= 1:
    print("⚠️  Some APIs are working. The app will run with limited features.")
    print()
    print("To enable all features, check the failed APIs above.")
else:
    print("❌ No APIs are working. Please check your API keys.")
    print()
    print("See API_SETUP_GUIDE.md for help getting API keys.")

print()
print("=" * 70)
