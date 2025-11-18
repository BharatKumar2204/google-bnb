#!/usr/bin/env python3
"""Test location news endpoint"""

import requests
import json

print("Testing Chennai location news...")
print()

# Chennai coordinates
lat = 13.0827
lng = 80.2707

try:
    response = requests.post(
        "http://localhost:8000/agents/map_intelligence",
        json={
            "lat": lat,
            "lng": lng,
            "radius_km": 25
        },
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print("Full Response:")
        print(json.dumps(data, indent=2))
        print()
        
        result = data.get('data', {})
        news = result.get('news', [])
        
        print(f"News count: {len(news)}")
        print(f"Area: {result.get('area', 'N/A')}")
        print()
        
        if news:
            print("News items:")
            for i, item in enumerate(news[:3], 1):
                print(f"{i}. {item.get('title', 'No title')}")
        else:
            print("❌ No news found!")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error: {str(e)}")
    print()
    print("Make sure backend is running:")
    print("  cd mcp_server && python run_server.py")
