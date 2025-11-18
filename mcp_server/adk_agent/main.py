#!/usr/bin/env python3
"""
AI News Verification MCP Server with Google ADK
Root Agent + 6 Specialized Agents + Real APIs
"""

import asyncio
import json
import logging
from typing import Dict, List
from datetime import datetime
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add parent directory to path for imports
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import all agents
from agents.news_fetch_agent import NewsFetchAgent
from agents.truth_verification_agent import TruthVerificationAgent
from agents.summary_context_agent import SummaryContextAgent
from agents.map_intelligence_agent import MapIntelligenceAgent
from agents.media_forensics_agent import MediaForensicsAgent
from agents.impact_relevance_agent import ImpactRelevanceAgent
from agents.metal_prices_agent import MetalPricesAgent # Import new agent

# Import Google ADK Agents
from adk_agent.root_agent import RootAgent

from config import Config, initialize_gcp_clients
from utils import logger, format_response

# ═════════════════════════════════════════════════════════════
# FASTAPI APP
# ═════════════════════════════════════════════════════════════

app = FastAPI(
    title="🤖 AI News Verification MCP Server with Google ADK",
    description="Root Agent + 6 Agents + Google Search Tool",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═════════════════════════════════════════════════════════════
# INITIALIZE
# ═════════════════════════════════════════════════════════════

config = Config()
try:
    gcp_clients = initialize_gcp_clients(config)
    logger.info("✅ GCP clients initialized")
except Exception as e:
    logger.warning(f"⚠️ GCP init skipped: {str(e)}")
    gcp_clients = {"config": config}

# ═════════════════════════════════════════════════════════════
# AGENT ORCHESTRATOR
# ═════════════════════════════════════════════════════════════

class AgentOrchestrator:
    """Orchestrates root agent and 6 specialized agents"""
    
    def __init__(self, config: Config, gcp_clients: Dict):
        self.config = config
        self.gcp_clients = gcp_clients
        self.logger = logger
        
        # Initialize Gemini Master Agent (primary AI agent)
        logger.info("🤖 Initializing Gemini Master Agent...")
        try:
            from agents.gemini_master_agent import GeminiMasterAgent
            self.gemini_agent = GeminiMasterAgent(config, gcp_clients)
            logger.info("✅ Gemini Master Agent initialized with function calling")
        except Exception as e:
            logger.warning(f"⚠️ Gemini Master Agent failed to initialize: {str(e)}")
            self.gemini_agent = None
        
        # Initialize 6 specialized agents (fallback)
        logger.info("🤖 Initializing 6 specialized agents...")
        
        self.agents = {
            "news_fetch": NewsFetchAgent(config, gcp_clients),
            "truth_verify": TruthVerificationAgent(config, gcp_clients),
            "summary": SummaryContextAgent(config, gcp_clients),
            "map_intel": MapIntelligenceAgent(config, gcp_clients),
            "media_forensics": MediaForensicsAgent(config, gcp_clients),
            "impact": ImpactRelevanceAgent(config, gcp_clients),
            "metal_prices": MetalPricesAgent(config, gcp_clients), # Initialize new agent
        }
        
        logger.info("✅ All 6 agents initialized")
        
        # Initialize Google ADK Root Agent
        logger.info("🤖 Initializing Google ADK Root Agent...")
        
        self.root_agent = RootAgent(config, gcp_clients, self.agents)
        
        logger.info("✅ Root Agent initialized with Google Search")
        logger.info(f"   Model: {self.root_agent.model_name}")
        logger.info(f"   Tools: {self.root_agent.tools}")

orchestrator = AgentOrchestrator(config, gcp_clients)

# ═════════════════════════════════════════════════════════════
# ROOT AGENT ENDPOINT
# ═════════════════════════════════════════════════════════════

@app.post("/agent/ask")
async def root_agent_ask(request: Request):
    """
    Main endpoint for Root Agent
    Uses Google ADK pattern with Google Search
    
    Request:
    {
        "query": "Is this news real?",
        "context": {...}  # optional
    }
    """
    try:
        payload = await request.json()
        query = payload.get("query", "")
        context = payload.get("context", {})
        
        logger.info(f"🤖 Root Agent Query: {query}")
        
        # Execute root agent
        result = await orchestrator.root_agent.process(query, context)
        
        return format_response("success", result)
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return format_response("error", {"message": str(e)}, error=True)

@app.post("/agent/search")
async def root_agent_search(request: Request):
    """
    Search endpoint for Root Agent
    Uses Google Search API
    """
    try:
        payload = await request.json()
        query = payload.get("query", "")
        
        logger.info(f"🔍 Search: {query}")
        
        # Execute search via root agent
        result = orchestrator.root_agent.google_search.execute(query)
        
        return format_response("success", result)
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return format_response("error", {"message": str(e)}, error=True)

# ═════════════════════════════════════════════════════════════
# SPECIALIZED AGENTS ENDPOINTS (unchanged from before)
# ═════════════════════════════════════════════════════════════

@app.post("/agents/news_fetch")
async def agent_news_fetch(request: Request):
    """Agent 1: News Fetch"""
    try:
        payload = await request.json()
        result = await orchestrator.agents["news_fetch"].execute(payload)
        return format_response("success", result)
    except Exception as e:
        return format_response("error", {"message": str(e)}, error=True)

@app.post("/agents/truth_verification")
async def agent_truth_verify(request: Request):
    """Agent 2: Truth Verification - Using Gemini Master Agent"""
    try:
        payload = await request.json()
        text = payload.get("text", "")
        
        logger.info(f"📝 Truth verification request: {text[:50]}...")
        
        # Use Gemini Master Agent for AI-powered verification
        if hasattr(orchestrator, 'gemini_agent') and orchestrator.gemini_agent:
            logger.info("🤖 Using Gemini Master Agent")
            result = await orchestrator.gemini_agent.analyze_text(text, task="verify")
            return format_response("success", result)
        else:
            # Fallback to original agent with Gemini
            logger.info("📊 Using Truth Verification Agent")
            result = await orchestrator.agents["truth_verify"].execute(payload)
            return format_response("success", result)
    except Exception as e:
        logger.error(f"❌ Truth verification error: {str(e)}")
        import traceback
        traceback.print_exc()
        return format_response("error", {"message": str(e)}, error=True)

@app.post("/agents/summary_context")
async def agent_summary(request: Request):
    """Agent 3: Summarization - Using Gemini Master Agent"""
    try:
        payload = await request.json()
        text = payload.get("text", "")
        
        # Use Gemini Master Agent for AI-powered summarization
        if hasattr(orchestrator, 'gemini_agent'):
            result = await orchestrator.gemini_agent.analyze_text(text, task="summarize")
            return format_response("success", result)
        else:
            # Fallback to original agent
            result = await orchestrator.agents["summary"].execute(payload)
            return format_response("success", result)
    except Exception as e:
        return format_response("error", {"message": str(e)}, error=True)

@app.post("/agents/map_intelligence")
async def agent_map_intel(request: Request):
    """Agent 4: Map Intelligence"""
    try:
        payload = await request.json()
        result = await orchestrator.agents["map_intel"].execute(payload)
        return format_response("success", result)
    except Exception as e:
        return format_response("error", {"message": str(e)}, error=True)

@app.post("/agents/media_forensics")
async def agent_media_forensics(request: Request):
    """Agent 5: Media Forensics - Using Gemini Master Agent"""
    try:
        payload = await request.json()
        media_url = payload.get("media_url", "")
        text = payload.get("text", "")
        
        # Use Gemini Master Agent for AI-powered image analysis
        if hasattr(orchestrator, 'gemini_agent') and media_url:
            result = await orchestrator.gemini_agent.analyze_image(media_url, text)
            return format_response("success", result)
        else:
            # Fallback to original agent
            result = await orchestrator.agents["media_forensics"].execute(payload)
            return format_response("success", result)
    except Exception as e:
        return format_response("error", {"message": str(e)}, error=True)

@app.post("/agents/impact_relevance")
async def agent_impact(request: Request):
    """Agent 6: Impact & Relevance"""
    try:
        payload = await request.json()
        result = await orchestrator.agents["impact"].execute(payload)
        return format_response("success", result)
    except Exception as e:
        return format_response("error", {"message": str(e)}, error=True)

@app.get("/agents/metal_prices")
async def agent_metal_prices():
    """Agent 7: Metal Prices"""
    try:
        result = await orchestrator.agents["metal_prices"].execute({})
        return format_response("success", result)
    except Exception as e:
        return format_response("error", {"message": str(e)}, error=True)

# ═════════════════════════════════════════════════════════════
# HEALTH & STATUS
# ═════════════════════════════════════════════════════════════

@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "✅ healthy",
        "service": "MCP Server v3.0",
        "root_agent": "Google ADK",
        "model": orchestrator.root_agent.model_name,
        "agents": list(orchestrator.agents.keys()),
        "tools": orchestrator.root_agent.tools
    }

@app.get("/")
async def root():
    """API Info"""
    return {
        "name": "🤖 AI News Verification MCP Server",
        "version": "3.0.0",
        "architecture": "Google ADK + Specialized Agents",
        "root_agent": {
            "name": orchestrator.root_agent.name,
            "model": orchestrator.root_agent.model_name,
            "description": orchestrator.root_agent.description,
            "tools": orchestrator.root_agent.tools
        },
        "specialized_agents": 6,
        "endpoints": {
            "root": "/agent/ask",
            "search": "/agent/search",
            "agents": [
                "/agents/news_fetch",
                "/agents/truth_verification",
                "/agents/summary_context",
                "/agents/map_intelligence",
                "/agents/media_forensics",
                "/agents/impact_relevance"
            ]
        }
    }

@app.get("/debug/root_agent")
async def debug_root_agent():
    """Debug root agent"""
    return {
        "root_agent": str(orchestrator.root_agent),
        "stats": orchestrator.root_agent.get_stats(),
        "description": orchestrator.root_agent.description,
        "instruction": orchestrator.root_agent.instruction,
        "retry_config": orchestrator.root_agent.retry_options
    }

# ═════════════════════════════════════════════════════════════
# STARTUP
# ═════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup():
    """Startup"""
    logger.info("=" * 70)
    logger.info("🚀 AI NEWS VERIFICATION MCP SERVER v3.0")
    logger.info("=" * 70)
    logger.info(f"🌍 Starting on {config.MCP_SERVER_HOST}:{config.MCP_SERVER_PORT}")
    logger.info(f"🤖 Root Agent: Google ADK + {orchestrator.root_agent.model_name}")
    logger.info(f"🔧 Tools: {orchestrator.root_agent.tools}")
    logger.info(f"📊 Specialized Agents: 6")
    logger.info("=" * 70)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.MCP_SERVER_HOST,
        port=config.MCP_SERVER_PORT,
        log_level="info"
    )
