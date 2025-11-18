project/
│
├── mcp_server/                          # MCP Server Directory
│   ├── main.py                          # Entry point (runs on port 8000)
│   ├── config.py                        # Configuration & environment setup
│   ├── utils.py                         # Shared utilities
│   ├── __init__.py
│   ├── .env                             # Google CLI credentials
│   ├── requirements.txt                 # Python dependencies
│   │
│   └── agents/
│       ├── __init__.py
│       ├── news_fetch_agent.py          # Agent 1: Fetches news from APIs
│       ├── truth_verification_agent.py  # Agent 2: Verifies authenticity
│       ├── summary_context_agent.py     # Agent 3: Summarizes & contextualizes
│       ├── map_intelligence_agent.py    # Agent 4: Geo-based news intelligence
│       ├── media_forensics_agent.py     # Agent 5: Analyzes images/videos
│       └── impact_relevance_agent.py    # Agent 6: Calculates impact score
│
└── adk_android/                         # Android ADK Client
    ├── build.gradle                     # Gradle build config
    ├── AndroidManifest.xml              # App manifest
    ├── config.properties                # API endpoints
    ├── .env                             # Firebase & GCP config
    │
    ├── MainActivity.java                # Entry activity
    ├── MCPClient.java                   # MCP HTTP/WebSocket client
    ├── NewsViewModel.java               # MVVM view model
    └── activity_main.xml                # UI layout
