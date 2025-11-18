"""
Root Agent using Google ADK
Coordinates all sub-agents with Gemini 2.5 Flash-Lite
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class RootAgent:
    """
    Root Agent using Google ADK pattern
    Orchestrates all agents and tools
    
    Properties:
    - model: Gemini 2.5 Flash-Lite
    - tools: Google Search
    - retry_options: Built-in retry logic
    - description: Helpful assistant for news verification
    """
    
    def __init__(self, config, gcp_clients, all_agents: Dict):
        self.name = "root_agent"
        self.model_name = "gemini-2.5-flash-lite"
        self.config = config
        self.gcp_clients = gcp_clients
        self.all_agents = all_agents
        self.logger = logging.getLogger("agent.root")
        
        # ADK Agent Configuration
        self.description = "A helpful assistant that can answer news and verification questions"
        self.instruction = """You are a helpful AI news assistant. 
        
Your capabilities:
1. Search current information using Google Search
2. Verify news authenticity
3. Summarize articles
4. Provide geo-based news
5. Analyze media for manipulation
6. Calculate relevance and impact

Use Google Search for:
- Current information not in your training data
- Fact verification
- Real-time news

For each user query:
1. Determine the best agent to use
2. Execute the agent
3. Return comprehensive results"""
        
        # Retry configuration
        self.retry_options = {
            "max_retries": 3,
            "initial_delay": 1.0,
            "backoff_multiplier": 2.0,
            "max_delay": 10.0
        }
        
        # Tools available
        self.tools = ["google_search", "news_fetch", "truth_verify", "summarize"]
        
        # Initialize Google Search
        from adk_agent.tool_manager import GoogleSearchTool
        self.google_search = GoogleSearchTool(
            config.GOOGLE_SEARCH_API_KEY if hasattr(config, 'GOOGLE_SEARCH_API_KEY') else None,
            config.GOOGLE_SEARCH_ENGINE_ID if hasattr(config, 'GOOGLE_SEARCH_ENGINE_ID') else None
        )
        
        self.stats = {"calls": 0, "errors": 0}
        
        logger.info("✅ Root Agent initialized")
        logger.info(f"   Model: {self.model_name}")
        logger.info(f"   Tools: {self.tools}")
        logger.info(f"   Retry: {self.retry_options['max_retries']} attempts")
    
    async def process(self, user_query: str, context: Dict = None) -> Dict:
        """
        Main entry point for root agent
        
        Args:
            user_query: User's input query
            context: Additional context (optional)
        
        Returns:
            Comprehensive response with agent results
        """
        try:
            self.logger.info(f"🤖 Root Agent: {user_query}")
            
            # Determine query type and route to appropriate agent
            query_type = self._determine_query_type(user_query)
            self.logger.info(f"   Query type: {query_type}")
            
            # Route to best agent
            result = await self._route_to_agent(query_type, user_query, context)
            
            self.stats["calls"] += 1
            
            return {
                "status": "success",
                "agent": "root_agent",
                "model": self.model_name,
                "query": user_query,
                "query_type": query_type,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.stats["errors"] += 1
            self.logger.error(f"Error: {str(e)}")
            raise
    
    def _determine_query_type(self, query: str) -> str:
        """Determine the type of query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["search", "find", "look for", "current"]):
            return "search"
        elif any(word in query_lower for word in ["verify", "true", "fake", "check", "authentic"]):
            return "verify"
        elif any(word in query_lower for word in ["summarize", "summary", "explain"]):
            return "summary"
        elif any(word in query_lower for word in ["where", "location", "map", "area"]):
            return "map"
        elif any(word in query_lower for word in ["image", "photo", "video", "media"]):
            return "media"
        else:
            return "general"
    
    async def _route_to_agent(self, query_type: str, query: str, context: Dict = None) -> Dict:
        """Route query to appropriate agent"""
        
        if query_type == "search":
            # Use Google Search
            return self.google_search.execute(query)
        
        elif query_type == "verify":
            # Use Truth Verification Agent
            agent = self.all_agents.get("truth_verify")
            if agent:
                return await agent.execute({
                    "text": query,
                    "article_id": "root_query"
                })
            return self.google_search.verify_claim(query)
        
        elif query_type == "summary":
            # Use Summary Agent
            agent = self.all_agents.get("summary")
            if agent:
                return await agent.execute({
                    "text": query,
                    "title": "User Query Summary"
                })
        
        elif query_type == "map":
            # Use Map Intelligence Agent
            agent = self.all_agents.get("map_intel")
            if agent:
                # Extract location from query
                location = context.get("location", {}) if context else {}
                return await agent.execute({
                    "lat": location.get("lat", 0),
                    "lng": location.get("lng", 0),
                    "radius_km": 25
                })
        
        elif query_type == "media":
            # Use Media Forensics Agent
            agent = self.all_agents.get("media_forensics")
            if agent and context and "media_url" in context:
                return await agent.execute({
                    "media_url": context["media_url"],
                    "media_type": context.get("media_type", "image")
                })
        
        # Default: General search
        return self.google_search.execute(query)
    
    def use_tool(self, tool_name: str, **kwargs) -> Dict:
        """Use a specific tool"""
        if tool_name == "google_search":
            return self.google_search.execute(kwargs.get("query", ""))
        elif tool_name == "verify_claim":
            return self.google_search.verify_claim(kwargs.get("claim", ""))
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def get_stats(self) -> Dict:
        return {
            **self.stats,
            "model": self.model_name,
            "tools": self.tools,
            "retry_config": self.retry_options
        }
    
    def __str__(self) -> str:
        return f"RootAgent(model={self.model_name}, tools={len(self.tools)}, retry_max={self.retry_options['max_retries']})"
