#!/usr/bin/env python3
"""
Quick test to check if backend is working
"""

import requests
import json

print("=" * 70)
print("🧪 BACKEND TEST")
print("=" * 70)
print()

BASE_URL = "http://localhost:8000"

# Test 1: Health Check
print("1️⃣  Testing Health Check...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print("   ✅ Backend is running!")
        data = response.json()
        print(f"   📊 Status: {data.get('status')}")
        print(f"   🤖 Agents: {len(data.get('agents', []))}")
    else:
        print(f"   ❌ Backend returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ❌ Cannot connect to backend!")
    print("   💡 Make sure backend is running:")
    print("      cd mcp_server")
    print("      python run_server.py")
    exit(1)
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    exit(1)

print()

# Test 2: Fetch News
print("2️⃣  Testing News Fetch...")
try:
    response = requests.post(
        f"{BASE_URL}/agents/news_fetch",
        json={"category": "technology", "limit": 5},
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        articles = data.get('data', {}).get('articles', [])
        print(f"   ✅ Got {len(articles)} articles")
        if articles:
            print(f"   📰 First article: {articles[0].get('title', 'N/A')[:50]}...")
            if 'mock' in data.get('data', {}):
                print("   ⚠️  Using mock data (API keys may not be configured)")
            else:
                print("   ✅ Using real data from NewsAPI!")
    else:
        print(f"   ❌ Status {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print()

# Test 3: Text Verification
print("3️⃣  Testing Text Verification...")
try:
    response = requests.post(
        f"{BASE_URL}/agents/truth_verification",
        json={
            "text": "Scientists discover new planet",
            "article_id": "test_1"
        },
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        score = data.get('data', {}).get('score', 0)
        verdict = data.get('data', {}).get('verdict', 'N/A')
        print(f"   ✅ Verification working!")
        print(f"   📊 Score: {score}/100")
        print(f"   ⚖️  Verdict: {verdict}")
    else:
        print(f"   ❌ Status {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print()

# Test 4: Map Intelligence
print("4️⃣  Testing Map Intelligence...")
try:
    response = requests.post(
        f"{BASE_URL}/agents/map_intelligence",
        json={
            "lat": 40.7128,
            "lng": -74.0060,
            "radius_km": 25
        },
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        news_count = len(data.get('data', {}).get('news', []))
        print(f"   ✅ Map intelligence working!")
        print(f"   📍 Found {news_count} news items")
    else:
        print(f"   ❌ Status {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print()
print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print()
print("If all tests passed:")
print("✅ Backend is working correctly")
print("✅ Frontend should show real data")
print()
print("If you see mock data warnings:")
print("⚠️  Check your API keys in mcp_server/.env")
print("⚠️  See YOUR_SETUP_GUIDE.md for API key setup")
print()
print("To view frontend console:")
print("1. Open http://localhost:3000")
print("2. Press F12 (Developer Tools)")
print("3. Click 'Console' tab")
print("4. Look for 🔄 and ✅ messages")
print()
print("=" * 70)
