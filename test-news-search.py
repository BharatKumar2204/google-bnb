import requests
import os
from dotenv import load_dotenv

load_dotenv('mcp_server/.env')

api_key = os.getenv('NEWS_API_KEY')
print(f"API Key: {api_key[:10]}...")

# Test search
url = "https://newsapi.org/v2/everything"
params = {
    "apiKey": api_key,
    "q": "AI breakthrough",
    "pageSize": 5,
    "sortBy": "publishedAt",
    "language": "en"
}

print(f"\n🔍 Testing NewsAPI search...")
response = requests.get(url, params=params, timeout=10)

print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Status: {data.get('status')}")
    print(f"Total Results: {data.get('totalResults')}")
    articles = data.get('articles', [])
    print(f"Articles returned: {len(articles)}")
    
    if articles:
        print("\n📰 First article:")
        print(f"Title: {articles[0].get('title')}")
        print(f"Source: {articles[0].get('source', {}).get('name')}")
        print(f"Published: {articles[0].get('publishedAt')}")
    else:
        print("⚠️ No articles found")
else:
    print(f"❌ Error: {response.text}")
