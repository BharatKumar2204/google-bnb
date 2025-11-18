"""
Agent 1: News Fetch Agent
Fetches news from multiple sources
"""

import logging
import requests
from typing import Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class NewsFetchAgent:
    def __init__(self, config, gcp_clients):
        self.config = config
        self.gcp_clients = gcp_clients
        self.logger = logging.getLogger("agent.news_fetch")
        self.cache = {} # Add a cache dictionary
        self.cache_expiry_time = timedelta(seconds=1) # Cache for 1 second for testing
        
    async def execute(self, payload: Dict) -> Dict:
        """Fetch news based on parameters"""
        try:
            category = payload.get("category", "all")
            limit = payload.get("limit", 20)
            url = payload.get("url")
            query = payload.get("query")
            
            if url:
                return await self._fetch_from_url(url)
            elif query:
                return await self._search_news(query, limit)
            else:
                # Check cache before fetching trending news
                cache_key = f"trending_{category}_{limit}"
                if cache_key in self.cache and datetime.now() < self.cache[cache_key]["expiry"]:
                    self.logger.info(f"✅ Serving trending news from cache for category: {category}")
                    return self.cache[cache_key]["data"]
                
                # Fetch and then store in cache
                news_data = await self._fetch_trending(category, limit)
                self.cache[cache_key] = {
                    "data": news_data,
                    "expiry": datetime.now() + self.cache_expiry_time
                }
                return news_data
                
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return {"error": str(e)}
    
    async def _fetch_trending(self, category: str, limit: int) -> Dict:
        """Fetch trending news"""
        try:
            if category == "world":
                return await self._search_news("world news", limit)

            # Use NewsAPI - try both possible env var names
            api_key = self.config.NEWS_API_KEY or self.config.GOOGLE_NEWS_API_KEY
            
            if not api_key:
                self.logger.warning("⚠️ No NewsAPI key found, returning empty list.")
                return {"articles": [], "total": 0, "category": category, "source": "error"}
            
            self.logger.info(f"📰 Fetching real news from NewsAPI (category: {category})")
            
            url = "https://newsapi.org/v2/top-headlines"
            
            if category == "all":
                category = "general"

            params = {
                "apiKey": api_key,
                "pageSize": limit * 2,  # Fetch more to account for ad filtering
                "language": "en",
                "country": "us",  # Add country for better results
                "category": category
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                self.logger.error(f"NewsAPI error: {response.status_code} - {response.text}")
                return {"articles": [], "total": 0, "category": category, "source": "error"}
            
            data = response.json()
            
            if data.get("status") != "ok":
                self.logger.error(f"NewsAPI returned error: {data.get('message')}")
                return {"articles": [], "total": 0, "category": category, "source": "error"}
            
            raw_articles = data.get("articles", [])
            
            # Filter out advertisements
            articles = []
            ads_filtered = 0
            
            for article in raw_articles:
                title = article.get("title", "")
                description = article.get("description", "")
                url = article.get("url", "")
                
                if self._is_advertisement(title, description, url):
                    ads_filtered += 1
                    self.logger.debug(f"🚫 Filtered ad: {title}")
                    continue
                
                articles.append(article)
                
                if len(articles) >= limit:
                    break
            
            self.logger.info(f"✅ Got {len(articles)} real articles from NewsAPI (filtered {ads_filtered} ads)")
            
            return {
                "articles": articles,
                "total": len(articles),
                "category": category,
                "source": "newsapi",
                "ads_filtered": ads_filtered
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching news: {str(e)}")
            return {"articles": [], "total": 0, "category": category, "source": "error"}
    
    async def _fetch_from_url(self, url: str) -> Dict:
        """Fetch article from URL"""
        try:
            # Validate URL format first
            if not url.startswith(('http://', 'https://')):
                return {
                    "error": "Invalid URL format",
                    "url": url,
                    "is_fake": True,
                    "reason": "URL must start with http:// or https://"
                }
            
            # Check for suspicious domains
            suspicious_domains = ['.test', '.example', '.invalid', '.localhost', 'florp-net']
            if any(domain in url.lower() for domain in suspicious_domains):
                return {
                    "error": "Suspicious or fake URL detected",
                    "url": url,
                    "is_fake": True,
                    "reason": "URL contains test/example domain"
                }
            
            self.logger.info(f"🔍 Attempting to fetch URL: {url}")
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            
            if response.status_code != 200:
                return {
                    "error": f"URL returned status code {response.status_code}",
                    "url": url,
                    "is_fake": False,
                    "reason": f"Server returned {response.status_code}"
                }
            
            # Simple content extraction (in production, use newspaper3k or similar)
            return {
                "url": url,
                "content": response.text[:5000],
                "title": "Article from URL",
                "fetched_at": datetime.now().isoformat(),
                "is_fake": False
            }
        except requests.exceptions.ConnectionError:
            return {
                "error": "Cannot connect to URL - domain may not exist",
                "url": url,
                "is_fake": True,
                "reason": "Connection failed - likely fake or non-existent domain"
            }
        except requests.exceptions.Timeout:
            return {
                "error": "URL request timed out",
                "url": url,
                "is_fake": False,
                "reason": "Server did not respond in time"
            }
        except Exception as e:
            return {
                "error": f"Failed to fetch URL: {str(e)}",
                "url": url,
                "is_fake": False,
                "reason": str(e)
            }
    
    def _is_advertisement(self, title: str, description: str, url: str) -> bool:
        """Detect if content is an advertisement"""
        text = f"{title} {description} {url}".lower()
        
        # Ad keywords and patterns
        ad_patterns = [
            # Direct ad indicators
            "sponsored", "advertisement", "promoted", "ad:", "[ad]", "(ad)",
            # Shopping/deals
            "buy now", "shop now", "order now", "get yours", "limited offer",
            "sale", "discount", "deal", "offer", "coupon", "promo",
            # Marketing language
            "click here", "learn more", "sign up", "subscribe now",
            "free trial", "best price", "lowest price", "save money",
            # Product marketing
            "product launch", "new product", "introducing", "now available",
            # Affiliate/referral
            "affiliate", "referral", "partner content",
            # Ad domains
            "doubleclick", "googleads", "adservice", "advertising"
        ]
        
        return any(pattern in text for pattern in ad_patterns)
    
    async def _search_news(self, query: str, limit: int) -> Dict:
        """Search for news by query using Google News RSS (Free, No API Key)"""
        try:
            self.logger.info(f"🔍 Searching Google News RSS for: {query}")
            
            # Use Google News RSS feed (free, no API key needed)
            import feedparser
            from urllib.parse import quote
            
            # Google News RSS URL
            encoded_query = quote(query)
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
            
            self.logger.info(f"📡 Fetching from: {rss_url}")
            
            # Parse RSS feed
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                self.logger.warning(f"⚠️ No articles found for query: {query}")
                return {"articles": [], "total": 0, "query": query}
            
            # Convert RSS entries to article format and filter ads
            articles = []
            ads_filtered = 0
            
            for entry in feed.entries[:limit * 2]:  # Fetch more to account for filtering
                # Extract source from title (Google News format: "Title - Source")
                title = entry.get('title', '')
                source_name = "Google News"
                
                if ' - ' in title:
                    parts = title.rsplit(' - ', 1)
                    title = parts[0]
                    source_name = parts[1] if len(parts) > 1 else source_name
                
                description = entry.get('summary', '')[:200]
                url = entry.get('link', '')
                
                # Filter out advertisements
                if self._is_advertisement(title, description, url):
                    ads_filtered += 1
                    self.logger.debug(f"🚫 Filtered ad: {title}")
                    continue
                
                article = {
                    "title": title,
                    "description": description,
                    "url": url,
                    "urlToImage": None,  # RSS doesn't provide images
                    "publishedAt": entry.get('published', datetime.now().isoformat()),
                    "source": {"name": source_name}
                }
                articles.append(article)
                
                if len(articles) >= limit:
                    break
            
            self.logger.info(f"✅ Found {len(articles)} articles from Google News RSS (filtered {ads_filtered} ads)")
            
            return {
                "articles": articles,
                "total": len(articles),
                "query": query,
                "source": "google_news_rss",
                "ads_filtered": ads_filtered
            }
            
        except Exception as e:
            self.logger.error(f"Error searching Google News RSS: {str(e)}")
            return {"articles": [], "total": 0, "query": query, "error": str(e)}
    
    def _get_mock_news(self, category: str, limit: int) -> Dict:
        """Return mock news for demo"""
        pass
