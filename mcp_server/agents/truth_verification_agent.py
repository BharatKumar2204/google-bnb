"""
Agent 2: Truth Verification Agent
Verifies news authenticity using fact-checking APIs and AI
"""

import logging
from typing import Dict, List
import google.generativeai as genai

logger = logging.getLogger(__name__)

class TruthVerificationAgent:
    def __init__(self, config, gcp_clients):
        self.config = config
        self.gcp_clients = gcp_clients
        self.logger = logging.getLogger("agent.truth_verify")
        
        # Initialize Gemini if API key available
        self.use_ai = False
        if hasattr(config, 'GEMINI_API_KEY') and config.GEMINI_API_KEY:
            try:
                api_key = config.GEMINI_API_KEY.strip('"').strip("'")
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.5-pro')
                self.use_ai = True
                self.logger.info("✅ Gemini 2.5 Pro enabled for verification")
            except Exception as e:
                self.logger.warning(f"⚠️ Gemini AI not available: {str(e)}")
        
    async def execute(self, payload: Dict) -> Dict:
        """Verify news authenticity"""
        try:
            text = payload.get("text", "")
            article_id = payload.get("article_id", "unknown")
            
            # Use AI verification if available
            if self.use_ai and len(text) > 20:
                self.logger.info("🤖 Using AI-powered verification")
                ai_result = await self._ai_verify(text)
                if ai_result:
                    return {
                        **ai_result,
                        "article_id": article_id,
                        "method": "ai_powered"
                    }
            
            # Fallback to rule-based analysis
            self.logger.info("📊 Using rule-based verification")
            score = self._calculate_credibility_score(text)
            verdict = self._get_verdict(score)
            sources = self._check_sources(text)
            
            return {
                "score": score,
                "verdict": verdict,
                "sources": sources,
                "article_id": article_id,
                "method": "rule_based",
                "analysis": {
                    "has_sources": len(sources) > 0,
                    "text_length": len(text),
                    "credibility_indicators": self._find_indicators(text)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return {"error": str(e)}
    
    async def _ai_verify(self, text: str) -> Dict:
        """Use Gemini AI for verification with Google Search fact-checking"""
        # First, use Google Search to find related information
        search_context = ""
        if hasattr(self.config, 'GOOGLE_SEARCH_API_KEY') and self.config.GOOGLE_SEARCH_API_KEY:
            try:
                import requests
                # Extract key claim from text for searching
                search_query = text[:200].replace('\n', ' ')
                
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    "key": self.config.GOOGLE_SEARCH_API_KEY,
                    "cx": self.config.GOOGLE_SEARCH_ENGINE_ID if hasattr(self.config, 'GOOGLE_SEARCH_ENGINE_ID') and self.config.GOOGLE_SEARCH_ENGINE_ID else "017576662512468239146:omuauf_lfve",
                    "q": search_query,
                    "num": 3
                }
                
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])
                    if items:
                        search_context = "\n\nRelated search results:\n"
                        for item in items[:3]:
                            search_context += f"- {item.get('title')}: {item.get('snippet')}\n"
                        self.logger.info(f"✅ Found {len(items)} related sources via Google Search")
            except Exception as e:
                self.logger.warning(f"Google Search failed: {str(e)}")
        
        prompt = f"""Analyze this news text for credibility and authenticity. 

Text to analyze:
{text[:1000]}
{search_context}

Provide:
1. A credibility score from 0-100 (where 100 is highly credible)
2. A verdict (Highly Credible, Likely Credible, Needs Verification, or Low Credibility)
3. Key credibility indicators found
4. Any red flags or concerns
5. Cross-reference with search results if provided

Respond in this exact format:
SCORE: [number]
VERDICT: [verdict]
INDICATORS: [comma-separated list]
CONCERNS: [concerns or "None"]
FACT_CHECK: [brief fact-check summary]
"""
        
        response = self.model.generate_content(prompt)
        result_text = response.text
        
        # Parse AI response
        score = 50  # default
        verdict = "Needs Verification"
        indicators = []
        concerns = "None"
        
        for line in result_text.split('\n'):
            if line.startswith('SCORE:'):
                try:
                    score = int(line.split(':')[1].strip())
                except:
                    pass
            elif line.startswith('VERDICT:'):
                verdict = line.split(':', 1)[1].strip()
            elif line.startswith('INDICATORS:'):
                indicators = [i.strip() for i in line.split(':', 1)[1].split(',')]
            elif line.startswith('CONCERNS:'):
                concerns = line.split(':', 1)[1].strip()
        
        self.logger.info(f"✅ AI Verification: Score={score}, Verdict={verdict}")
        
        return {
            "score": score,
            "verdict": verdict,
            "sources": self._check_sources(text),
            "analysis": {
                "has_sources": True,
                "text_length": len(text),
                "credibility_indicators": indicators,
                "ai_concerns": concerns,
                "ai_analysis": result_text
            }
        }
    
    def _calculate_credibility_score(self, text: str) -> int:
        """Calculate credibility score (0-100)"""
        score = 50  # Base score
        
        # Check for credibility indicators
        indicators = {
            "according to": 5,
            "study shows": 5,
            "research": 5,
            "expert": 5,
            "official": 5,
            "confirmed": 5,
            "reported": 3,
            "sources say": 3
        }
        
        text_lower = text.lower()
        for indicator, points in indicators.items():
            if indicator in text_lower:
                score += points
        
        # Penalize sensational language
        sensational = ["shocking", "unbelievable", "you won't believe", "miracle"]
        for word in sensational:
            if word in text_lower:
                score -= 10
        
        return max(0, min(100, score))
    
    def _get_verdict(self, score: int) -> str:
        """Get verdict based on score"""
        if score >= 80:
            return "Highly Credible"
        elif score >= 60:
            return "Likely Credible"
        elif score >= 40:
            return "Needs Verification"
        else:
            return "Low Credibility"
    
    def _check_sources(self, text: str) -> List[Dict]:
        """Extract and verify sources"""
        # Simplified source detection
        sources = []
        
        known_sources = [
            {"name": "Reuters", "reliability": "High"},
            {"name": "AP News", "reliability": "High"},
            {"name": "BBC", "reliability": "High"},
            {"name": "CNN", "reliability": "Medium"},
            {"name": "Fox News", "reliability": "Medium"}
        ]
        
        text_lower = text.lower()
        for source in known_sources:
            if source["name"].lower() in text_lower:
                sources.append({
                    "name": source["name"],
                    "reliability": source["reliability"],
                    "url": f"https://{source['name'].lower().replace(' ', '')}.com"
                })
        
        return sources
    
    def _find_indicators(self, text: str) -> List[str]:
        """Find credibility indicators"""
        indicators = []
        text_lower = text.lower()
        
        checks = {
            "Has citations": any(word in text_lower for word in ["according to", "study", "research"]),
            "Has quotes": '"' in text,
            "Has dates": any(word in text_lower for word in ["today", "yesterday", "2024", "2025"]),
            "Professional tone": not any(word in text_lower for word in ["shocking", "unbelievable"])
        }
        
        for check, passed in checks.items():
            if passed:
                indicators.append(check)
        
        return indicators
