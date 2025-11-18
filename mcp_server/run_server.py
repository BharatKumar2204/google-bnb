#!/usr/bin/env python3
"""
Startup script for AI News Verification MCP Server
Run this from the mcp_server directory
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Now import and run the main app
from adk_agent.main import app, config

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("🚀 AI NEWS VERIFICATION MCP SERVER v3.0")
    print("=" * 70)
    print(f"🌍 Starting on {config.MCP_SERVER_HOST}:{config.MCP_SERVER_PORT}")
    print("=" * 70)
    
    uvicorn.run(
        app,
        host=config.MCP_SERVER_HOST,
        port=config.MCP_SERVER_PORT,
        log_level="info"
    )
