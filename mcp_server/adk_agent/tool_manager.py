"""
Tool Manager for Google ADK
Manages Google Search and other tools
"""

import logging
import requests
from typing import Dict, List

logger = logging.getLogger(__name__)

class GoogleSearchTool:
    """Google Search Tool for Root Agent"""
    
    def __init__(self, api_key: str, engine_id: str):
        self.api_key = api_key
        self.engine_id = engine_id
        self.logger = logging.getLogger("tool.google_search")
        
    def execute(self, query: str, num_results: int = 5) -> Dict:
        """Execute Google Search"""
        try:
            if not self.api_key or not self.engine_id:
                return self._mock_search(query)
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.api_key,
                "cx": self.engine_id,
                "q": query,
                "num": num_results
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            results = []
            for item in data.get("items", []):
                results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                })
            
            return {
                "query": query,
                "results": results,
                "total": len(results)
            }
            
        except Exception as e:
            self.logger.error(f"Search error: {str(e)}")
            return self._mock_search(query)
    
    def verify_claim(self, claim: str) -> Dict:
        """Verify a claim using search"""
        search_results = self.execute(f"fact check {claim}")
        
        return {
            "claim": claim,
            "verification": "Needs manual review",
            "sources": search_results.get("results", [])
        }
    
    def _mock_search(self, query: str) -> Dict:
        """Return mock search results"""
        return {
            "query": query,
            "results": [
                {
                    "title": f"Search result for: {query}",
                    "link": "https://example.com/result1",
                    "snippet": "This is a mock search result for demonstration purposes."
                },
                {
                    "title": f"More information about {query}",
                    "link": "https://example.com/result2",
                    "snippet": "Additional context and information about the search query."
                }
            ],
            "total": 2,
            "mock": True
        }
