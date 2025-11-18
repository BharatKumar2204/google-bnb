"""
Utility functions for MCP Server
"""

import logging
from typing import Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("mcp_server")

def format_response(status: str, data: Any, error: bool = False) -> Dict:
    """Format API response"""
    return {
        "status": status,
        "data": data,
        "error": error
    }
