"""
Deep Analysis Agent
Enhanced news analysis with keyword extraction, source scoring, and comprehensive verification
"""

import logging
import re
from typing import Dict, List
import google.generativeai as genai
import feedparser
from urllib.parse import quote

logger = logging.getLogger(__name__)

class DeepAnalysisAgent:
    def __init__(self, config, gcp_clients):
        self.config = config
        self.gcp_clients = gcp_clients
        self.logger = logging.getLogger("agent.deep_analysis")
        
        # Initialize Gemini AI
        self.use_ai = False
        if hasattr(config, 'GEMINI_API_KEY') and config.GEMINI_API_KEY:
            try:
                api_key = config.GEMINI_API_KEY.strip('"').strip("'")
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.5-pro')
                self.use_ai = True
                self.logger.info("✅ Gemini 2.5 Pro enabled for deep analysis")
            except Exception as e:
                self.logger.warning(f"⚠️ Gemini AI not available: {str(e)}")
    
    def _extract_keywords(self, headline: str) -> List[str]:
        """Extract meaningful keywords from headline using AI or rules"""
        if self.use_ai:
            try:
                prompt = f"""Extract 3-5 key search terms from this headline for finding related news articles.
Focus on:
- Main entities (people, organizations, places)
- Key events or actions
- Important topics

Headline: {headline}

Return ONLY the keywords separated by commas, nothing else."""
                
                response = self.model.generate_content(prompt)
                keywords = [k.strip() for k in response.text.split(',')]
                self.logger.info(f"🔑 AI extracted keywords: {keywords}")
                return keywords
            except Exception as e:
                self.logger.warning(f"AI keyword extraction failed: {e}")
        
        # Fallback: Rule-based keyword extraction
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'been', 'be',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                     'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        
        # Extract words, keep capitalized words and longer words
        words = re.findall(r'\b[A-Z][a-z]+\b|\b\w{4,}\b', headline)
        keywords = [w for w in words if w.lower() not in stop_words]
        
        # Take top 5 unique keywords
        keywords = list(dict.fromkeys(keywords))[:5]
        self.logger.info(f"🔑 Rule-based keywords: {keywords}")
        return keywords
    
    def _is_advertisement(self, title: str, description: str, url: str) -> bool:
        """Detect if content is an advertisement"""
        text = f"{title} {description} {url}".lower()
        
        ad_patterns = [
            "sponsored", "advertisement", "promoted", "ad:", "[ad]", "(ad)",
            "buy now", "shop now", "order now", "get yours", "limited offer",
            "sale", "discount", "deal", "offer", "coupon", "promo",
            "click here", "learn more", "sign up", "subscribe now",
            "free trial", "best price", "lowest price", "save money",
            "product launch", "new product", "introducing", "now available",
            "affiliate", "referral", "partner content",
            "doubleclick", "googleads", "adservice", "advertising"
        ]
        
        return any(pattern in text for pattern in ad_patterns)
    
    def _calculate_source_score(self, articles: List[Dict]) -> Dict:
        """Calculate credibility score based on number and quality of sources"""
        if not articles:
            return {
                "score": 5,
                "verdict": "No Sources Found",
                "reason": "No credible news sources found covering this topic"
            }
        
        # Source reliability ratings
        high_reliability = ['reuters', 'ap news', 'bbc', 'associated press', 'npr', 
                           'the guardian', 'the new york times', 'washington post']
        medium_reliability = ['cnn', 'fox news', 'msnbc', 'abc news', 'cbs news', 
                             'nbc news', 'usa today', 'bloomberg']
        
        num_sources = len(articles)
        high_quality_count = 0
        medium_quality_count = 0
        
        for article in articles:
            source_name = article.get('source', {}).get('name', '').lower()
            if any(reliable in source_name for reliable in high_reliability):
                high_quality_count += 1
            elif any(reliable in source_name for reliable in medium_reliability):
                medium_quality_count += 1
        
        # Calculate score based on number of sources:
        # 1 source = 5%, 2 = 10%, 3 = 15%, ... 10+ = 40% base
        if num_sources == 1:
            base_score = 5
        elif num_sources == 2:
            base_score = 10
        elif num_sources == 3:
            base_score = 15
        elif num_sources == 4:
            base_score = 20
        elif num_sources == 5:
            base_score = 25
        elif num_sources == 6:
            base_score = 30
        elif num_sources == 7:
            base_score = 33
        elif num_sources == 8:
            base_score = 36
        elif num_sources == 9:
            base_score = 38
        else:  # 10 or more
            base_score = 40
        
        # Quality bonus: high reliability sources boost score significantly
        quality_bonus = (high_quality_count * 15) + (medium_quality_count * 8)
        
        total_score = min(base_score + quality_bonus, 100)
        
        # Determine verdict
        if total_score >= 80:
            verdict = "Highly Credible - Multiple Reliable Sources"
        elif total_score >= 60:
            verdict = "Credible - Multiple Sources Found"
        elif total_score >= 40:
            verdict = "Moderately Credible - Limited Sources"
        elif total_score >= 20:
            verdict = "Low Credibility - Few Sources"
        else:
            verdict = "Unverifiable - Insufficient Sources"
        
        reason = f"Found {num_sources} source(s)"
        if high_quality_count > 0:
            reason += f", including {high_quality_count} high-reliability source(s)"
        if medium_quality_count > 0:
            reason += f" and {medium_quality_count} medium-reliability source(s)"
        
        self.logger.info(f"📊 Source Score: {total_score}/100 - {verdict}")
        
        return {
            "score": total_score,
            "verdict": verdict,
            "reason": reason,
            "source_count": num_sources,
            "high_quality_sources": high_quality_count,
            "medium_quality_sources": medium_quality_count
        }
    
    async def search_news(self, headline: str, limit: int = 10) -> List[Dict]:
        """Search for news using extracted keywords"""
        # Extract keywords
        keywords = self._extract_keywords(headline)
        
        if not keywords:
            self.logger.warning("No keywords extracted, using full headline")
            keywords = [headline]
        
        # Build search query with keywords
        search_query = ' '.join(keywords[:3])  # Use top 3 keywords
        self.logger.info(f"🔍 Searching with query: {search_query}")
        
        # Search Google News RSS
        try:
            encoded_query = quote(search_query)
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
            
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                self.logger.warning(f"⚠️ No articles found for: {search_query}")
                return []
            
            # Convert RSS entries to article format and filter ads
            articles = []
            ads_filtered = 0
            
            for entry in feed.entries[:limit * 2]:  # Fetch more to account for filtering
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
                    continue
                
                articles.append({
                    "title": title,
                    "description": description,
                    "url": url,
                    "publishedAt": entry.get('published', ''),
                    "source": {"name": source_name}
                })
                
                if len(articles) >= limit:
                    break
            
            self.logger.info(f"✅ Found {len(articles)} articles (filtered {ads_filtered} ads)")
            return articles
            
        except Exception as e:
            self.logger.error(f"Error searching news: {str(e)}")
            return []
    
    async def execute(self, payload: Dict) -> Dict:
        """Execute deep analysis on a headline or topic"""
        try:
            headline = payload.get("headline", "")
            
            if not headline:
                return {"error": "No headline provided"}
            
            self.logger.info(f"🔍 Deep Analysis: {headline}")
            
            # Step 1: Search for related news
            articles = await self.search_news(headline, limit=10)
            
            # Step 2: Calculate source-based credibility score
            source_analysis = self._calculate_source_score(articles)
            
            # Step 3: Generate AI summary if articles found
            summary = ""
            key_points = []
            
            if articles and self.use_ai:
                combined_text = '\n\n'.join([
                    f"{article['title']}\n{article.get('description', '')}"
                    for article in articles[:5]
                ])
                
                prompt = f"""Analyze these news articles about: {headline}

Articles:
{combined_text}

Provide:
1. A comprehensive 3-4 sentence summary
2. 4-6 key points (bullet format)
3. Overall assessment of the situation

Format:
SUMMARY: [summary]
KEY_POINTS:
- [point 1]
- [point 2]
...
ASSESSMENT: [assessment]"""
                
                try:
                    response = self.model.generate_content(prompt)
                    result_text = response.text
                    
                    # Parse response
                    lines = result_text.split('\n')
                    current_section = None
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('SUMMARY:'):
                            summary = line.split(':', 1)[1].strip()
                        elif line.startswith('KEY_POINTS:'):
                            current_section = 'points'
                        elif line.startswith('ASSESSMENT:'):
                            assessment = line.split(':', 1)[1].strip()
                            current_section = None
                        elif current_section == 'points' and line.startswith('-'):
                            key_points.append(line[1:].strip())
                    
                    self.logger.info("✅ AI summary generated")
                except Exception as e:
                    self.logger.error(f"AI summary failed: {e}")
                    summary = f"Found {len(articles)} news articles covering this topic from various sources."
            else:
                summary = f"Found {len(articles)} news articles covering this topic."
            
            return {
                "headline": headline,
                "summary": summary,
                "key_points": key_points or [f"Found {len(articles)} related articles"],
                "verification_score": source_analysis["score"],
                "verdict": source_analysis["verdict"],
                "source_analysis": source_analysis,
                "related_news": articles,
                "keywords_used": self._extract_keywords(headline)
            }
            
        except Exception as e:
            self.logger.error(f"Error in deep analysis: {str(e)}")
            return {"error": str(e)}
