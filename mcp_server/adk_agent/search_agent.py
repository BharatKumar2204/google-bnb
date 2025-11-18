"""
Search Agent using Google ADK
Uses Google Search tool and Gemini 2.5 Flash-Lite
"""

import logging
import json
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class SearchAgent:
    """Search Agent with Google ADK integration"""
    
    def __init__(self, config, gcp_clients):
        self.name = "SearchAgent"
        self.config = config
        self.gcp_clients = gcp_clients
        self.logger = logging.getLogger("agent.search")
        self.stats = {"calls": 0, "errors": 0}
        
        # Initialize Google Search Tool
        from mcp_server.adk_agents.tool_manager import GoogleSearchTool
        self.search_tool = GoogleSearchTool(
            config.GOOGLE_SEARCH_API_KEY,
            config.GOOGLE_SEARCH_ENGINE_ID
        )
        
        # Initialize Gemini Flash Lite for fast processing
        self.model_id = config.VERTEX_FLASH_LITE_MODEL
    
    async def execute(self, payload: Dict) -> Dict:
        """Execute search using Google ADK pattern"""
        query = payload.get("query", "")
        search_type = payload.get("search_type", "general")
        
        try:
            self.logger.info(f"🔍 Search Agent: {query}")
            
            # Execute search based on type
            if search_type == "news":
                search_results = self.search_tool.search_current_news(query)
            elif search_type == "verify":
                search_results = self.search_tool.verify_claim(query)
            else:
                search_results = self.search_tool.execute(query)
            
            if search_results.get("status") != "success":
                raise Exception(f"Search failed: {search_results.get('error')}")
            
            # Process results with Gemini Flash Lite
            processed_results = await self._process_with_gemini(
                query,
                search_results.get("results", [])
            )
            
            self.stats["calls"] += 1
            
            return {
                "agent": "search",
                "query": query,
                "search_type": search_type,
                "raw_results_count": len(search_results.get("results", [])),
                "processed_results": processed_results,
                "status": "success"
            }
            
        except Exception as e:
            self.stats["errors"] += 1
            self.logger.error(f"Error: {str(e)}")
            raise
    
    async def _process_with_gemini(self, query: str, results: List[Dict]) -> List[Dict]:
        """Process search results with Gemini Flash Lite"""
        try:
            from vertexai.generative_models import GenerativeModel
            
            model = GenerativeModel(self.model_id)
            
            # Summarize each result
            processed = []
            for result in results[:5]:
                prompt = f"""Summarize this search result briefly:
Title: {result.get('title', '')}
Link: {result.get('link', '')}
Snippet: {result.get('snippet', '')}

Provide a 2-sentence summary."""
                
                try:
                    response = model.generate_content(prompt)
                    processed.append({
                        "title": result.get("title"),
                        "link": result.get("link"),
                        "snippet": result.get("snippet"),
                        "summary": response.text.strip()
                    })
                except:
                    processed.append(result)
            
            return processed
            
        except Exception as e:
            self.logger.error(f"Gemini processing error: {str(e)}")
            return results[:5]
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
