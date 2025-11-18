"""
Agent 6: Impact & Relevance Agent
Calculates impact score and relevance using Gemini AI
"""

import logging
from typing import Dict
import google.generativeai as genai

logger = logging.getLogger(__name__)

class ImpactRelevanceAgent:
    def __init__(self, config, gcp_clients):
        self.config = config
        self.gcp_clients = gcp_clients
        self.logger = logging.getLogger("agent.impact")
        
        # Initialize Gemini AI
        self.use_ai = False
        if hasattr(config, 'GEMINI_API_KEY') and config.GEMINI_API_KEY:
            try:
                api_key = config.GEMINI_API_KEY.strip('"').strip("'")
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.5-pro')
                self.use_ai = True
                self.logger.info("✅ Gemini 2.5 Pro enabled for impact analysis")
            except Exception as e:
                self.logger.warning(f"⚠️ Gemini AI not available: {str(e)}")
        
    async def execute(self, payload: Dict) -> Dict:
        """Calculate impact and relevance"""
        try:
            text = payload.get("text", "")
            context = payload.get("context", "")
            
            # Use AI if available
            if self.use_ai and len(text) > 20:
                self.logger.info("🤖 Using AI-powered impact analysis")
                ai_result = await self._ai_analyze_impact(text, context)
                if ai_result:
                    return {
                        **ai_result,
                        "method": "ai_powered"
                    }
            
            # Fallback to rule-based
            self.logger.info("📊 Using rule-based impact analysis")
            impact_score = self._calculate_impact(text)
            relevance = self._assess_relevance(text, context)
            reach = self._estimate_reach(text)
            
            return {
                "impact_score": impact_score,
                "relevance": relevance,
                "estimated_reach": reach,
                "factors": self._get_impact_factors(text),
                "method": "rule_based"
            }
            
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return {"error": str(e)}
    
    async def _ai_analyze_impact(self, text: str, context: str) -> Dict:
        """Use Gemini AI for impact analysis"""
        try:
            prompt = f"""Analyze the impact and relevance of this news:

Text: {text[:1000]}
Context: {context}

Provide:
1. Impact Score (0-100): How significant is this news?
2. Relevance: How current and relevant is this?
3. Estimated Reach: Who will this affect?
4. Urgency Level: How urgent is this news?
5. Scope: Local, National, or Global?

Respond in this format:
IMPACT_SCORE: [number 0-100]
RELEVANCE: [description]
REACH: [description]
URGENCY: [High/Medium/Low]
SCOPE: [Local/National/Global]
REASONING: [brief explanation]
"""
            
            response = self.model.generate_content(prompt)
            result_text = response.text
            
            # Parse response
            impact_score = 50
            relevance = "Moderate Relevance"
            reach = "Regional"
            urgency = "Medium"
            scope = "National"
            reasoning = ""
            
            for line in result_text.split('\n'):
                if line.startswith('IMPACT_SCORE:'):
                    try:
                        impact_score = int(line.split(':')[1].strip())
                    except:
                        pass
                elif line.startswith('RELEVANCE:'):
                    relevance = line.split(':', 1)[1].strip()
                elif line.startswith('REACH:'):
                    reach = line.split(':', 1)[1].strip()
                elif line.startswith('URGENCY:'):
                    urgency = line.split(':', 1)[1].strip()
                elif line.startswith('SCOPE:'):
                    scope = line.split(':', 1)[1].strip()
                elif line.startswith('REASONING:'):
                    reasoning = line.split(':', 1)[1].strip()
            
            self.logger.info(f"✅ AI Impact Analysis: Score={impact_score}, Urgency={urgency}")
            
            return {
                "impact_score": impact_score,
                "relevance": relevance,
                "estimated_reach": reach,
                "factors": {
                    "urgency": urgency,
                    "scope": scope,
                    "reasoning": reasoning
                }
            }
            
        except Exception as e:
            self.logger.error(f"AI impact analysis failed: {str(e)}")
            return None
    
    def _calculate_impact(self, text: str) -> int:
        """Calculate impact score (0-100)"""
        score = 50  # Base score
        text_lower = text.lower()
        
        # High impact keywords
        high_impact = ["breaking", "urgent", "critical", "major", "significant", "historic"]
        for word in high_impact:
            if word in text_lower:
                score += 10
        
        # Scope indicators
        scope_words = ["global", "national", "worldwide", "international"]
        for word in scope_words:
            if word in text_lower:
                score += 5
        
        return min(100, score)
    
    def _assess_relevance(self, text: str, context: str) -> str:
        """Assess relevance"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["today", "now", "current", "latest"]):
            return "Highly Relevant - Current Event"
        elif any(word in text_lower for word in ["recent", "this week", "yesterday"]):
            return "Relevant - Recent News"
        else:
            return "Moderate Relevance"
    
    def _estimate_reach(self, text: str) -> str:
        """Estimate potential reach"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["global", "worldwide", "international"]):
            return "Global (Millions)"
        elif any(word in text_lower for word in ["national", "country"]):
            return "National (Hundreds of thousands)"
        else:
            return "Local/Regional (Thousands)"
    
    def _get_impact_factors(self, text: str) -> Dict:
        """Get factors contributing to impact"""
        text_lower = text.lower()
        
        return {
            "urgency": "High" if "breaking" in text_lower else "Medium",
            "scope": "Global" if "global" in text_lower else "Local",
            "topic_importance": "High" if any(w in text_lower for w in ["health", "safety", "security"]) else "Medium"
        }
