# FACT-X - AI-Powered Truth Discovery & News Intelligence

A comprehensive news verification and analysis platform powered by Google Gemini 2.5 Pro AI, featuring location-based news discovery, real-time verification, and intelligent summarization.

## 🌟 Overview

This application combines multiple AI agents to provide real-time news verification, location-based news discovery, and intelligent content analysis. Built with React (frontend) and FastAPI (backend), it leverages Google's Gemini 2.5 Pro for advanced AI capabilities.

## 🎯 Key Features

### 1. **Trending News Dashboard**
- Real-time news feed from Google News RSS (no API key required)
- Category filtering (All, Technology, Business, Sports, etc.)
- Clean card-based UI with source attribution
- Click to read full articles

### 2. **Quick AI Summary**
- Enter any news headline or topic
- Automatically searches Google News RSS for related articles
- AI-powered summary generation using Gemini 2.5 Pro
- Displays related news articles with images and metadata
- Credibility scoring for news topics

### 3. **Text Analysis**
- Paste any news text or article content
- AI verification using Gemini 2.5 Pro
- Credibility score (0-100%)
- Key points extraction
- Impact and relevance analysis
- Source verification

### 4. **Location-Based News**
- Interactive map interface (Leaflet.js)
- Click anywhere on the map to find local news
- Search by location name (e.g., "Chennai", "Bangalore")
- Keyword filtering for specific topics
- News categorized by domain:
  - ⚽ Sports
  - 🏛️ Politics
  - 💼 Business
  - 💻 Technology
  - 🎬 Entertainment
  - 🏥 Health
  - 🔬 Science
- Adjustable search radius (5-100 km)
- Only shows news from last 2 days
- Scrollable sidebar with categorized news
- No markers on map for clean visualization

## 🏗️ Architecture

### Backend (FastAPI + Python)
```
mcp_server/
├── agents/
│   ├── news_fetch_agent.py          # Fetches news from Google News RSS
│   ├── truth_verification_agent.py  # Verifies content with Gemini 2.5 Pro
│   ├── summary_context_agent.py     # Generates AI summaries
│   ├── impact_relevance_agent.py    # Analyzes impact and relevance
│   ├── map_intelligence_agent.py    # Location-based news discovery
│   └── gemini_master_agent.py       # Master AI orchestrator
├── run_server.py                     # FastAPI server
└── requirements.txt                  # Python dependencies
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.jsx            # Main dashboard with tabs
│   │   ├── TrendingNews.jsx         # Trending news feed
│   │   ├── QuickSummary.jsx         # Quick summary feature
│   │   ├── InputPanel.jsx           # Text analysis input
│   │   ├── ResultsPanel.jsx         # Analysis results display
│   │   └── MapSearch.jsx            # Location-based news map
│   ├── services/
│   │   └── api.js                   # API service layer
│   └── App.jsx                      # Root component
└── package.json                     # Node dependencies
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- Google Cloud Project with Gemini API enabled

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd ai-news-app/mcp_server
```

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
Create/edit `.env` file:
```env
# Google Gemini AI
GEMINI_API_KEY="your-gemini-api-key"

# Google Cloud (Optional)
GCP_PROJECT_ID="your-project-id"
GOOGLE_APPLICATION_CREDENTIALS="credentials.json"

# Server Configuration
MCP_SERVER_HOST="localhost"
MCP_SERVER_PORT="8000"
DEBUG="True"
```

4. **Start the backend server:**
```bash
python run_server.py
```

Server will run on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd ai-news-app/frontend
```

2. **Install Node dependencies:**
```bash
npm install
```

3. **Configure environment:**
Create `.env` file:
```env
VITE_API_URL=http://localhost:8000
```

4. **Start the development server:**
```bash
npm run dev
```

Frontend will run on `http://localhost:5173`

## 📖 Usage Guide

### Trending News
1. Open the application
2. Default tab shows trending news
3. Use category filters to narrow down topics
4. Click any article to read the full story

### Quick AI Summary
1. Click "Quick Summary" tab
2. Enter a headline or topic (e.g., "AI breakthrough", "Climate summit")
3. Click "Summarize with AI"
4. View:
   - AI-generated incident summary
   - Related news articles from Google News
   - Credibility score

### Text Analysis
1. Click "Text Analysis" tab
2. Paste news text or article content
3. Click "Analyze"
4. Get:
   - Verification score (0-100%)
   - AI verdict (Highly Credible, Needs Verification, etc.)
   - Key points extraction
   - Impact analysis

### Location-Based News
1. Click "Location News" tab
2. Either:
   - Click anywhere on the map
   - Search for a location (e.g., "Chennai")
   - Use "Current Location" button
3. Optional: Enter keyword filter (e.g., "sports", "politics")
4. Adjust search radius (5-100 km)
5. View categorized news in the right sidebar

## 🔧 Technical Details

### AI Agents

#### 1. News Fetch Agent
- **Purpose**: Fetches news from multiple sources
- **Data Source**: Google News RSS (free, no API key)
- **Features**:
  - Search by query
  - Category filtering
  - Location-based search
  - RSS feed parsing with feedparser

#### 2. Truth Verification Agent
- **Purpose**: Verifies news authenticity
- **AI Model**: Google Gemini 2.5 Pro
- **Features**:
  - Credibility scoring (0-100%)
  - Source verification
  - Fact-checking with Google Search
  - Red flag detection
  - Fake URL detection

#### 3. Summary Context Agent
- **Purpose**: Generates intelligent summaries
- **AI Model**: Google Gemini 2.5 Pro
- **Features**:
  - Key points extraction
  - Context-aware summarization
  - Multi-article synthesis

#### 4. Impact Relevance Agent
- **Purpose**: Analyzes news impact
- **AI Model**: Google Gemini 2.5 Pro
- **Features**:
  - Impact scoring
  - Relevance assessment
  - Audience analysis

#### 5. Map Intelligence Agent
- **Purpose**: Location-based news discovery
- **Features**:
  - Reverse geocoding (OpenStreetMap)
  - Radius-based search
  - News categorization by domain
  - Date filtering (last 2 days)
  - Keyword filtering

### Key Technologies

**Backend:**
- FastAPI - Modern Python web framework
- Google Gemini 2.5 Pro - Advanced AI model
- feedparser - RSS feed parsing
- requests - HTTP client
- python-dotenv - Environment management

**Frontend:**
- React 18 - UI framework
- Vite - Build tool
- Leaflet.js - Interactive maps
- React-Leaflet - React bindings for Leaflet
- Lucide React - Icon library
- Axios - HTTP client

### API Endpoints

```
POST /agents/news_fetch
- Fetch trending news or search by query
- Body: { category?, query?, limit? }

POST /agents/truth_verification
- Verify news content
- Body: { text, article_id }

POST /agents/summary_context
- Generate AI summary
- Body: { text, title }

POST /agents/impact_relevance
- Analyze impact and relevance
- Body: { text, context }

POST /agents/map_intelligence
- Get location-based news
- Body: { lat, lng, radius_km, keyword? }
```

## 🎨 UI Features

### Design Highlights
- Modern gradient-based color scheme (purple/blue)
- Responsive grid layouts
- Smooth animations and transitions
- Card-based content display
- Interactive map with custom markers
- Categorized news with emoji icons
- Clean, minimal interface

### User Experience
- Tab-based navigation
- Real-time loading states
- Error handling with user-friendly messages
- Clickable news cards
- Scrollable content areas
- Mobile-responsive design

## 🔐 Security Features

1. **Fake URL Detection**
   - Validates URL format
   - Detects test/example domains
   - Connection verification
   - Low credibility scores for fake URLs

2. **Content Verification**
   - AI-powered fact-checking
   - Source reliability assessment
   - Cross-reference with Google Search
   - Sensational language detection

3. **Date Filtering**
   - Only shows recent news (last 2 days)
   - Timezone-aware date handling
   - Prevents outdated information

## 📊 Data Flow

### Quick Summary Flow
```
User Input (Headline)
    ↓
Google News RSS Search
    ↓
Parse RSS Feed (feedparser)
    ↓
Extract Articles
    ↓
Combine Article Content
    ↓
Gemini 2.5 Pro Analysis
    ↓
Generate Summary + Verification
    ↓
Display Results
```

### Location News Flow
```
User Clicks Map / Searches Location
    ↓
Reverse Geocoding (OpenStreetMap)
    ↓
Build Search Query (Location + Keyword)
    ↓
Google News RSS Search
    ↓
Filter by Date (Last 2 Days)
    ↓
Categorize by Domain (AI-based)
    ↓
Display in Sidebar (Categorized)
```

## 🌐 Data Sources

### Primary Sources
1. **Google News RSS** (Free, No API Key)
   - URL: `https://news.google.com/rss/search?q={query}`
   - Format: RSS/XML
   - Coverage: Global news
   - Update Frequency: Real-time

2. **OpenStreetMap Nominatim** (Free)
   - Reverse geocoding
   - Location search
   - No API key required

### AI Services
1. **Google Gemini 2.5 Pro**
   - Text analysis
   - Summarization
   - Verification
   - Requires API key

2. **Google Custom Search** (Optional)
   - Fact-checking
   - Source verification
   - Requires API key

## 🐛 Troubleshooting

### Backend Issues

**Issue: "No NewsAPI key found"**
- Solution: Using Google News RSS (no key needed)
- This is informational, not an error

**Issue: "Gemini AI not available"**
- Check GEMINI_API_KEY in .env
- Verify API key is valid
- Ensure Gemini API is enabled in Google Cloud

**Issue: "Date parsing error"**
- Fixed with timezone-aware datetime
- Should not affect functionality

### Frontend Issues

**Issue: "Failed to fetch"**
- Ensure backend is running on port 8000
- Check VITE_API_URL in frontend/.env
- Verify CORS is enabled in backend

**Issue: "Map not loading"**
- Check internet connection (Leaflet uses CDN)
- Verify Leaflet CSS is imported
- Check browser console for errors

**Issue: "No news found"**
- Try different search terms
- Check internet connection
- Verify Google News RSS is accessible

## 📝 Development Notes

### Recent Improvements
1. Switched from NewsAPI to Google News RSS (free, no limits)
2. Added fake URL detection with low credibility scores
3. Implemented timezone-aware date filtering
4. Added news categorization by domain
5. Removed URL input from Quick Summary (simplified UX)
6. Added keyword filtering for location news
7. Implemented 2-day news filter
8. Created clean map visualization without markers

### Future Enhancements
- Add user authentication
- Implement news bookmarking
- Add social media integration
- Create mobile app version
- Add more news sources
- Implement caching for better performance
- Add news alerts/notifications

## 📄 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your needs.

## 📧 Support

For issues or questions, please check the troubleshooting section above.

---

**Built with ❤️ using Google Gemini 2.5 Pro AI**
