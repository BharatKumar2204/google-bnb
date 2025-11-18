"""
Master Gemini Agent
Uses Gemini 2.5 Pro with function calling to analyze text/images
and verify facts using Google Search and Fact Check APIs
"""

import logging
import google.generativeai as genai
from typing import Dict, List, Optional
import requests
import json

logger = logging.getLogger(__name__)

class GeminiMasterAgent:
    """
    Main AI agent powered by Gemini 2.5 Pro
    Uses function calling to access verification tools
    """
    
    def __init__(self, config, gcp_clients):
        self.config = config
        self.gcp_clients = gcp_clients
        self.logger = logging.getLogger("agent.gemini_master")
        
        # Initialize Gemini 2.5 Pro
        if not hasattr(config, 'GEMINI_API_KEY') or not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in config")
        
        api_key = config.GEMINI_API_KEY.strip('"').strip("'")
        genai.configure(api_key=api_key)
        
        # Use Gemini 2.5 Pro with function calling
        self.model = genai.GenerativeModel(
            'gemini-2.5-pro',
            tools=[self._get_tools()]
        )
        
        self.logger.info("✅ Gemini Master Agent initialized with gemini-2.5-pro and function calling")
    
    def _get_tools(self):
        """Define tools that Gemini can use"""
        return [
            {
                "function_declarations": [
                    {
                        "name": "google_search",
                        "description": "Search Google to verify facts and find related information",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The search query to verify facts"
                                }
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "fact_check",
                        "description": "Check if a claim has been fact-checked by reputable sources",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "claim": {
                                    "type": "string",
                                    "description": "The claim to fact-check"
                                }
                            },
                            "required": ["claim"]
                        }
                    }
                ]
            }
        ]
    
    async def analyze_text(self, text: str, task: str = "verify") -> Dict:
        """
        Analyze text using Gemini with tool calling
        
        Args:
            text: Text to analyze
            task: Type of analysis (verify, summarize, analyze)
        """
        try:
            self.logger.info(f"🤖 Gemini analyzing text (task: {task})")
            
            # Create prompt based on task
            if task == "verify":
                prompt = f"""Analyze this text for credibility and authenticity.

Text: {text}

Tasks:
1. Assess credibility (score 0-100)
2. Identify key claims that need verification
3. Use google_search tool to verify important claims
4. Use fact_check tool if specific claims are made
5. Provide verdict: Highly Credible, Likely Credible, Needs Verification, or Low Credibility
6. List credibility indicators and concerns

Provide detailed analysis with evidence from your searches."""

            elif task == "summarize":
                prompt = f"""Summarize and analyze this text.

Text: {text}

Tasks:
1. Create a concise 2-3 sentence summary
2. Extract 3-5 key points
3. Identify main topics
4. Assess sentiment (Positive/Negative/Neutral)
5. Determine complexity (Simple/Medium/Complex)
6. Use google_search if you need context about unfamiliar topics

Provide comprehensive analysis."""

            else:  # general analysis
                prompt = f"""Analyze this text comprehensively.

Text: {text}

Tasks:
1. Verify credibility using google_search
2. Summarize key points
3. Assess impact and relevance
4. Check for misinformation using fact_check
5. Provide actionable insights

Use all available tools to provide thorough analysis."""

            # Start chat with Gemini
            chat = self.model.start_chat()
            response = chat.send_message(prompt)
            
            # Handle function calls
            while response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call
                function_name = function_call.name
                function_args = dict(function_call.args)
                
                self.logger.info(f"🔧 Gemini calling tool: {function_name}")
                
                # Execute the function
                if function_name == "google_search":
                    result = self._google_search(function_args["query"])
                elif function_name == "fact_check":
                    result = self._fact_check(function_args["claim"])
                else:
                    result = {"error": "Unknown function"}
                
                # Send result back to Gemini
                response = chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=function_name,
                                response={"result": result}
                            )
                        )]
                    )
                )
            
            # Get final response
            final_response = response.text
            self.logger.info("✅ Gemini analysis complete")
            
            # Parse response based on task
            return self._parse_response(final_response, task)
            
        except Exception as e:
            self.logger.error(f"❌ Gemini analysis failed: {str(e)}")
            raise
    
    async def analyze_image(self, image_url: str, text: str = "") -> Dict:
        """
        Analyze image using Gemini Vision
        
        Args:
            image_url: URL of image to analyze
            text: Optional text context
        """
        try:
            self.logger.info("🖼️ Gemini analyzing image")
            
            # Use Gemini 2.5 Pro for image analysis (has vision capabilities)
            vision_model = genai.GenerativeModel('gemini-2.5-pro')
            
            prompt = f"""Analyze this image for authenticity and manipulation.

{f'Context: {text}' if text else ''}

Tasks:
1. Describe what you see in the image
2. Check for signs of manipulation or editing
3. Assess authenticity (score 0-100)
4. Identify any red flags
5. Use google_search to verify if this image appears elsewhere
6. Provide verdict on image authenticity

Be thorough and use available tools."""

            # Download image
            response = requests.get(image_url, timeout=10)
            image_data = response.content
            
            # Analyze with Gemini
            chat = vision_model.start_chat()
            response = chat.send_message([prompt, {"mime_type": "image/jpeg", "data": image_data}])
            
            result = response.text
            self.logger.info("✅ Image analysis complete")
            
            return self._parse_image_response(result)
            
        except Exception as e:
            self.logger.error(f"❌ Image analysis failed: {str(e)}")
            raise
    
    def _google_search(self, query: str) -> Dict:
        """Execute Google Search"""
        try:
            self.logger.info(f"🔍 Searching Google: {query}")
            
            if not hasattr(self.config, 'GOOGLE_SEARCH_API_KEY') or not self.config.GOOGLE_SEARCH_API_KEY:
                return {"error": "Google Search API key not configured"}
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": self.config.GOOGLE_SEARCH_API_KEY.strip('"').strip("'"),
                "cx": getattr(self.config, 'GOOGLE_SEARCH_ENGINE_ID', '017576662512468239146:omuauf_lfve'),
                "q": query,
                "num": 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                results = []
                for item in items:
                    results.append({
                        "title": item.get('title'),
                        "snippet": item.get('snippet'),
                        "link": item.get('link')
                    })
                
                self.logger.info(f"✅ Found {len(results)} search results")
                return {"results": results, "total": len(results)}
            else:
                return {"error": f"Search failed: {response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Search error: {str(e)}")
            return {"error": str(e)}
    
    def _fact_check(self, claim: str) -> Dict:
        """Check claim using Google Fact Check API"""
        try:
            self.logger.info(f"✓ Fact-checking: {claim[:50]}...")
            
            if not hasattr(self.config, 'GOOGLE_FACT_CHECK_API_KEY') or not self.config.GOOGLE_FACT_CHECK_API_KEY:
                return {"error": "Fact Check API key not configured"}
            
            url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
            params = {
                "key": self.config.GOOGLE_FACT_CHECK_API_KEY.strip('"').strip("'"),
                "query": claim
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                claims = data.get('claims', [])
                
                if claims:
                    fact_checks = []
                    for claim_data in claims[:3]:
                        fact_checks.append({
                            "claim": claim_data.get('text'),
                            "claimant": claim_data.get('claimant'),
                            "rating": claim_data.get('claimReview', [{}])[0].get('textualRating'),
                            "publisher": claim_data.get('claimReview', [{}])[0].get('publisher', {}).get('name')
                        })
                    
                    self.logger.info(f"✅ Found {len(fact_checks)} fact-checks")
                    return {"fact_checks": fact_checks, "found": True}
                else:
                    return {"fact_checks": [], "found": False, "message": "No fact-checks found"}
            else:
                return {"error": f"Fact check failed: {response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Fact check error: {str(e)}")
            return {"error": str(e)}
    
    def _parse_response(self, response: str, task: str) -> Dict:
        """Parse Gemini's response into structured data"""
        # Extract key information from response
        result = {
            "analysis": response,
            "method": "gemini_ai_with_tools"
        }
        
        # Try to extract score if present
        if "score" in response.lower() or "/100" in response:
            import re
            score_match = re.search(r'(\d+)/100|score[:\s]+(\d+)', response, re.IGNORECASE)
            if score_match:
                score = int(score_match.group(1) or score_match.group(2))
                result["score"] = score
                
                # Determine verdict based on score
                if score >= 80:
                    result["verdict"] = "Highly Credible"
                elif score >= 60:
                    result["verdict"] = "Likely Credible"
                elif score >= 40:
                    result["verdict"] = "Needs Verification"
                else:
                    result["verdict"] = "Low Credibility"
        
        return result
    
    def _parse_image_response(self, response: str) -> Dict:
        """Parse image analysis response"""
        return {
            "analysis": response,
            "method": "gemini_vision_with_tools"
        }
