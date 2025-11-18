"""
Agent 4: Map Intelligence Agent
Provides geo-based news intelligence
"""

import logging
from typing import Dict, List
from datetime import datetime
import math
import requests

logger = logging.getLogger(__name__)

class MapIntelligenceAgent:
    def __init__(self, config, gcp_clients):
        self.config = config
        self.gcp_clients = gcp_clients
        self.logger = logging.getLogger("agent.map_intel")
        
    async def execute(self, payload: Dict) -> Dict:
        """Get location-based news"""
        try:
            lat = payload.get("lat", 0)
            lng = payload.get("lng", 0)
            radius_km = payload.get("radius_km", 25)
            keyword = payload.get("keyword", None)
            
            # Get country from lat/lng
            country = await self._get_country_from_lat_lng(lat, lng)
            
            # Find news within radius
            news = await self._find_nearby_news(country, lat, lng, radius_km, keyword)
            
            # Filter by date (last 2 days)
            news = self._filter_by_date(news, days=2)
            
            # Categorize news
            categorized_news = self._categorize_news(news)
            
            area_info = self._get_area_info(lat, lng)
            
            return {
                "news": news,
                "categorized_news": categorized_news,
                "area": area_info["name"],
                "nearby_events": len(news),
                "radius_km": radius_km,
                "center": {"lat": lat, "lng": lng},
                "summary": f"Found {len(news)} news items within {radius_km}km of {area_info['name']}"
            }
            
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return {"error": str(e)}

    async def _get_country_from_lat_lng(self, lat: float, lng: float) -> str:
        """Get country from latitude and longitude using a reverse geocoding API."""
        try:
            # Using a free reverse geocoding API
            url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}"
            headers = {
                'User-Agent': 'AI News Verification App'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get('address', {}).get('country_code', 'us').upper()
        except Exception as e:
            self.logger.error(f"Could not get country from lat/lng: {e}")
            return "us"

    async def _find_nearby_news(self, country: str, lat: float, lng: float, radius_km: float, keyword: str = None) -> List[Dict]:
        """Find news using NewsAPI and Google Search."""
        all_news = []
        
        # Get area name for better search
        area_name = self._get_area_name(lat, lng)
        search_query = f"{keyword} {area_name}" if keyword else area_name
        self.logger.info(f"📍 Searching news for: {search_query}")
        
        # Method 1: Search NewsAPI by location name (works better than country code)
        api_key = (getattr(self.config, 'NEWS_API_KEY', None) or 
                   getattr(self.config, 'GOOGLE_NEWS_API_KEY', None))
        
        if api_key:
            api_key = api_key.strip('"').strip("'")
            try:
                # Use Google News RSS (Free, No API Key)
                import feedparser
                from urllib.parse import quote
                
                encoded_query = quote(search_query)
                rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
                
                self.logger.info(f"📰 Searching Google News RSS for: {search_query}")
                feed = feedparser.parse(rss_url)
                
                if feed.entries:
                    self.logger.info(f"✅ Found {len(feed.entries)} articles from Google News RSS")
                    
                    for i, entry in enumerate(feed.entries[:20]):
                        # Extract source from title
                        title = entry.get('title', '')
                        source_name = "Google News"
                        
                        if ' - ' in title:
                            parts = title.rsplit(' - ', 1)
                            title = parts[0]
                            source_name = parts[1] if len(parts) > 1 else source_name
                        
                        all_news.append({
                            "title": title,
                            "description": entry.get("summary", "")[:200],
                            "location": {"lat": lat + (i * 0.01), "lng": lng + (i * 0.01)},
                            "distance_km": round(i * 2.5, 1),
                            "publishedAt": entry.get("published", datetime.now().isoformat()),
                            "url": entry.get("link"),
                            "source": source_name,
                            "source_type": "Google News RSS"
                        })
                else:
                    self.logger.warning(f"⚠️ No articles found from Google News RSS")
                    
            except Exception as e:
                self.logger.error(f"Google News RSS search failed: {str(e)}")
        
        # Method 2: Use Google Search for additional local news
        search_key = getattr(self.config, 'GOOGLE_SEARCH_API_KEY', None)
        if search_key and len(all_news) < 5:
            search_key = search_key.strip('"').strip("'")
            try:
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    "key": search_key,
                    "cx": getattr(self.config, 'GOOGLE_SEARCH_ENGINE_ID', '017576662512468239146:omuauf_lfve'),
                    "q": f"news {search_query} latest",
                    "num": 10
                }
                
                self.logger.info(f"🔍 Searching Google for: news {search_query}")
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])
                    self.logger.info(f"✅ Found {len(items)} results from Google")
                    
                    for i, item in enumerate(items):
                        all_news.append({
                            "title": item.get('title'),
                            "description": item.get('snippet'),
                            "location": {"lat": lat - (i * 0.01), "lng": lng - (i * 0.01)},
                            "distance_km": round((i + 1) * 3.0, 1),
                            "publishedAt": datetime.now().isoformat(),
                            "url": item.get('link'),
                            "source": "Google Search",
                            "source_type": "Google"
                        })
                else:
                    self.logger.error(f"Google Search error: {response.status_code}")
                    
            except Exception as e:
                self.logger.error(f"Google Search failed: {str(e)}")
        
        self.logger.info(f"📊 Total news found: {len(all_news)}")
        return all_news
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two points in km (Haversine formula)"""
        R = 6371  # Earth's radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lng = math.radians(lng2 - lng1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _get_area_name(self, lat: float, lng: float) -> str:
        """Get area name from coordinates using reverse geocoding"""
        try:
            import requests
            # Use OpenStreetMap Nominatim for reverse geocoding (free)
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                "lat": lat,
                "lon": lng,
                "format": "json"
            }
            headers = {
                "User-Agent": "NewsVerificationApp/1.0"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                address = data.get('address', {})
                
                # Try to get city, town, or village name
                area = (address.get('city') or 
                       address.get('town') or 
                       address.get('village') or
                       address.get('county') or
                       address.get('state'))
                
                if area:
                    country = address.get('country', '')
                    return f"{area}, {country}" if country else area
            
        except Exception as e:
            self.logger.warning(f"Reverse geocoding failed: {str(e)}")
        
        # Fallback to coordinates
        return f"Location ({lat:.2f}, {lng:.2f})"
    
    def _get_area_info(self, lat: float, lng: float) -> Dict:
        """Get area information"""
        area_name = self._get_area_name(lat, lng)
        return {
            "name": area_name,
            "type": "urban",
            "population": "Unknown"
        }
    
    def _filter_by_date(self, news: List[Dict], days: int = 2) -> List[Dict]:
        """Filter news to only include items from last N days"""
        from datetime import datetime, timedelta, timezone
        
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        filtered_news = []
        
        for item in news:
            try:
                published = item.get('publishedAt')
                if published:
                    # Parse ISO format date
                    if isinstance(published, str):
                        pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    else:
                        pub_date = published
                    
                    # Make sure pub_date is timezone-aware
                    if pub_date.tzinfo is None:
                        pub_date = pub_date.replace(tzinfo=timezone.utc)
                    
                    if pub_date >= cutoff_date:
                        filtered_news.append(item)
                else:
                    # Include if no date (assume recent)
                    filtered_news.append(item)
            except Exception as e:
                self.logger.warning(f"Date parsing error: {e}")
                # Include if date parsing fails
                filtered_news.append(item)
        
        self.logger.info(f"📅 Filtered to {len(filtered_news)} news items from last {days} days")
        return filtered_news
    
    def _categorize_news(self, news: List[Dict]) -> Dict[str, List[Dict]]:
        """Categorize news by domain (Sports, Politics, etc.)"""
        categories = {
            "Sports": [],
            "Politics": [],
            "Business": [],
            "Technology": [],
            "Entertainment": [],
            "Health": [],
            "Science": [],
            "Other": []
        }
        
        # Keywords for each category
        category_keywords = {
            "Sports": ["cricket", "football", "soccer", "tennis", "sports", "match", "tournament", "player", "team", "game", "championship"],
            "Politics": ["government", "minister", "election", "parliament", "political", "party", "vote", "policy", "law", "congress"],
            "Business": ["economy", "market", "stock", "business", "company", "trade", "finance", "investment", "corporate", "industry"],
            "Technology": ["tech", "technology", "software", "app", "digital", "ai", "computer", "internet", "startup", "innovation"],
            "Entertainment": ["movie", "film", "actor", "music", "celebrity", "entertainment", "show", "concert", "festival", "cinema"],
            "Health": ["health", "medical", "hospital", "doctor", "disease", "covid", "vaccine", "patient", "treatment", "medicine"],
            "Science": ["science", "research", "study", "scientist", "discovery", "space", "climate", "environment", "energy"]
        }
        
        for item in news:
            title = (item.get('title') or '').lower()
            description = (item.get('description') or '').lower()
            text = f"{title} {description}"
            
            categorized = False
            for category, keywords in category_keywords.items():
                if any(keyword in text for keyword in keywords):
                    categories[category].append(item)
                    categorized = True
                    break
            
            if not categorized:
                categories["Other"].append(item)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
