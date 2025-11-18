# Complete Code Explanation

## Project Overview

This is a news verification and discovery platform that uses Google's Gemini AI to analyze news credibility and provides location-based news discovery. The application has two main parts: a React frontend and a Python FastAPI backend.

---

## Architecture

```
User Browser (React)
        ↓
    API Calls (HTTP)
        ↓
FastAPI Backend (Python)
        ↓
    AI Agents
        ↓
External Services (Google News RSS, Gemini AI)
```

---

## Backend Structure

### 1. Server Entry Point (`run_server.py`)

**Purpose**: Starts the FastAPI server

```python
from adk_agent.main import app, config
import uvicorn

uvicorn.run(
    app,
    host=config.MCP_SERVER_HOST,  # localhost
    port=config.MCP_SERVER_PORT,  # 8000
    log_level="info"
)
```

**What it does**:
- Imports the FastAPI app from `adk_agent/main.py`
- Starts the server on localhost:8000
- Enables logging for debugging

---

### 2. Main Application (`adk_agent/main.py`)

**Purpose**: Core FastAPI application with all API endpoints

#### Key Components:

**FastAPI App Setup**:
```python
app = FastAPI(
    title="AI News Verification MCP Server",
    description="Root Agent + 6 Agents",
    version="3.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
```

**Agent Orchestrator**:
```python
class AgentOrchestrator:
    def __init__(self, config, gcp_clients):
        # Initialize 6 specialized agents
        self.agents = {
            "news_fetch": NewsFetchAgent(...),
            "truth_verify": TruthVerificationAgent(...),
            "summary": SummaryContextAgent(...),
            "map_intel": MapIntelligenceAgent(...),
            "media_forensics": MediaForensicsAgent(...),
            "impact": ImpactRelevanceAgent(...)
        }
        
        # Initialize root agent for orchestration
        self.root_agent = RootAgent(...)
```

**What it does**:
- Creates instances of all 6 specialized agents
- Each agent handles a specific task
- Root agent coordinates between agents

#### API Endpoints:

**1. News Fetch Endpoint**:
```python
@app.post("/agents/news_fetch")
async def agent_news_fetch(request: Request):
    payload = await request.json()
    result = await orchestrator.agents["news_fetch"].execute(payload)
    return {"status": "success", "data": result}
```

**Input**: `{ "category": "technology", "limit": 100 }`
**Output**: List of news articles from Google News RSS

**2. Truth Verification Endpoint**:
```python
@app.post("/agents/truth_verification")
async def agent_truth_verify(request: Request):
    payload = await request.json()
    text = payload.get("text", "")
    
    # Use Gemini AI for verification
    result = await orchestrator.gemini_agent.analyze_text(text, task="verify")
    return {"status": "success", "data": result}
```

**Input**: `{ "text": "News article content..." }`
**Output**: Credibility score (0-100%), verdict, analysis

**3. Summary Endpoint**:
```python
@app.post("/agents/summary_context")
async def agent_summary(request: Request):
    payload = await request.json()
    text = payload.get("text", "")
    
    # Use Gemini AI for summarization
    result = await orchestrator.gemini_agent.analyze_text(text, task="summarize")
    return {"status": "success", "data": result}
```

**Input**: `{ "text": "Long article...", "title": "Article Title" }`
**Output**: Summary, key points

**4. Map Intelligence Endpoint**:
```python
@app.post("/agents/map_intelligence")
async def agent_map_intel(request: Request):
    payload = await request.json()
    result = await orchestrator.agents["map_intel"].execute(payload)
    return {"status": "success", "data": result}
```

**Input**: `{ "lat": 13.08, "lng": 80.27, "radius_km": 25, "keyword": "sports" }`
**Output**: Categorized news from that location

---

### 3. Specialized Agents

#### A. News Fetch Agent (`agents/news_fetch_agent.py`)

**Purpose**: Fetches news from Google News RSS

**Key Method**:
```python
async def _search_news(self, query: str, limit: int):
    # Build Google News RSS URL
    encoded_query = quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}"
    
    # Parse RSS feed
    feed = feedparser.parse(rss_url)
    
    # Extract articles
    articles = []
    for entry in feed.entries[:limit]:
        title = entry.get('title', '')
        
        # Google News format: "Title - Source"
        if ' - ' in title:
            parts = title.rsplit(' - ', 1)
            title = parts[0]
            source_name = parts[1]
        
        articles.append({
            "title": title,
            "description": entry.get('summary', ''),
            "url": entry.get('link', ''),
            "publishedAt": entry.get('published', ''),
            "source": {"name": source_name}
        })
    
    return {"articles": articles}
```

**How it works**:
1. Takes a search query (e.g., "AI breakthrough")
2. Builds Google News RSS URL
3. Parses XML feed using feedparser
4. Extracts title, description, URL, date, source
5. Returns structured article data

**Why Google News RSS?**
- Free (no API key needed)
- No rate limits
- Real-time news
- Global coverage

---

#### B. Truth Verification Agent (`agents/truth_verification_agent.py`)

**Purpose**: Verifies news credibility using Gemini AI

**Key Method**:
```python
async def _ai_verify(self, text: str):
    prompt = f"""Analyze this news text for credibility.

Text: {text}

Provide:
1. Credibility score (0-100)
2. Verdict (Highly Credible, Needs Verification, Low Credibility)
3. Key indicators
4. Red flags

Format:
SCORE: [number]
VERDICT: [verdict]
INDICATORS: [list]
CONCERNS: [concerns]
"""
    
    # Call Gemini AI
    response = self.model.generate_content(prompt)
    
    # Parse response
    score = extract_score(response.text)
    verdict = extract_verdict(response.text)
    
    return {
        "score": score,
        "verdict": verdict,
        "analysis": response.text
    }
```

**How it works**:
1. Takes news text as input
2. Creates a detailed prompt for Gemini AI
3. Sends to Gemini 2.5 Pro
4. Parses AI response
5. Returns credibility score and analysis

**Scoring Logic**:
- 80-100%: Highly Credible
- 60-79%: Likely Credible
- 40-59%: Needs Verification
- 0-39%: Low Credibility

---

#### C. Map Intelligence Agent (`agents/map_intelligence_agent.py`)

**Purpose**: Finds location-based news and categorizes it

**Key Methods**:

**1. Get Location Name**:
```python
def _get_area_name(self, lat: float, lng: float):
    # Reverse geocoding using OpenStreetMap
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {"lat": lat, "lon": lng, "format": "json"}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract city/town name
    address = data.get('address', {})
    area = address.get('city') or address.get('town')
    country = address.get('country', '')
    
    return f"{area}, {country}"  # e.g., "Chennai, India"
```

**2. Search News**:
```python
async def _find_nearby_news(self, search_query: str):
    # Build RSS URL with location
    rss_url = f"https://news.google.com/rss/search?q={search_query}"
    
    # Parse feed
    feed = feedparser.parse(rss_url)
    
    # Extract articles
    news = []
    for entry in feed.entries:
        news.append({
            "title": entry.title,
            "description": entry.summary,
            "url": entry.link,
            "publishedAt": entry.published
        })
    
    return news
```

**3. Filter by Date**:
```python
def _filter_by_date(self, news, days=2):
    from datetime import datetime, timedelta, timezone
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
    filtered = []
    
    for item in news:
        pub_date = datetime.fromisoformat(item['publishedAt'])
        
        if pub_date >= cutoff_date:
            filtered.append(item)
    
    return filtered
```

**4. Categorize News**:
```python
def _categorize_news(self, news):
    categories = {
        "Sports": [],
        "Politics": [],
        "Business": [],
        "Technology": [],
        "Entertainment": [],
        "Health": [],
        "Science": [],
        "Other": []
    }
    
    # Keywords for each category
    category_keywords = {
        "Sports": ["cricket", "football", "ipl", "nba", ...],
        "Technology": ["ai", "tech", "google", "apple", ...],
        # ... more categories
    }
    
    # Categorize each article
    for item in news:
        text = f"{item['title']} {item['description']}".lower()
        
        categorized = False
        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                categories[category].append(item)
                categorized = True
                break
        
        if not categorized:
            categories["Other"].append(item)
    
    return categories
```

**Complete Flow**:
```
User clicks map at (13.08, 80.27)
    ↓
Reverse geocode → "Chennai, India"
    ↓
Search Google News RSS for "Chennai, India"
    ↓
Get 20 articles
    ↓
Filter to last 2 days → 13 articles
    ↓
Categorize by keywords:
    Sports: 5 articles
    Politics: 3 articles
    Business: 5 articles
    ↓
Return categorized news
```

---

## Frontend Structure

### 1. Main App (`frontend/src/App.jsx`)

**Purpose**: Root component

```jsx
function App() {
  return (
    <div className="App">
      <Dashboard />
    </div>
  )
}
```

Simple wrapper that renders the Dashboard component.

---

### 2. Dashboard (`frontend/src/components/Dashboard.jsx`)

**Purpose**: Main container with tab navigation

```jsx
const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('trending')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const tabs = [
    { id: 'trending', label: 'Trending News', icon: TrendingUp },
    { id: 'summary', label: 'Quick Summary', icon: Sparkles },
    { id: 'text', label: 'Text Analysis', icon: FileText },
    { id: 'map', label: 'Location News', icon: MapPin }
  ]

  return (
    <div className="dashboard">
      {/* Tab Navigation */}
      <nav className="dashboard-nav">
        {tabs.map(tab => (
          <button
            className={activeTab === tab.id ? 'active' : ''}
            onClick={() => setActiveTab(tab.id)}
          >
            <Icon /> {tab.label}
          </button>
        ))}
      </nav>

      {/* Content */}
      {activeTab === 'trending' && <TrendingNews />}
      {activeTab === 'summary' && <QuickSummary />}
      {activeTab === 'text' && <InputPanel type="text" />}
      {activeTab === 'map' && <MapSearch />}
    </div>
  )
}
```

**How it works**:
- Manages active tab state
- Renders appropriate component based on tab
- Passes loading/error states to children

---

### 3. Trending News (`frontend/src/components/TrendingNews.jsx`)

**Purpose**: Displays trending news with category filters

```jsx
const TrendingNews = () => {
  const [news, setNews] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState('all')

  const categories = ['all', 'world', 'technology', 'business', 'health', 'science']

  // Fetch news when component mounts or category changes
  useEffect(() => {
    fetchTrendingNews()
  }, [selectedCategory])

  const fetchTrendingNews = async () => {
    setLoading(true)
    
    // Call backend API
    const response = await api.fetchNews({ 
      category: selectedCategory, 
      limit: 100 
    })
    
    // Clean HTML from titles/descriptions
    const cleanedArticles = response.articles.map(article => ({
      ...article,
      title: stripHtml(article.title),
      description: stripHtml(article.description)
    }))
    
    // Shuffle and show 12 random articles
    const shuffled = shuffleArray(cleanedArticles)
    setNews(shuffled.slice(0, 12))
    
    setLoading(false)
  }

  const stripHtml = (html) => {
    const tmp = document.createElement('DIV')
    tmp.innerHTML = html
    return tmp.textContent || tmp.innerText || ''
  }

  const shuffleArray = (array) => {
    const shuffled = [...array]
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    }
    return shuffled
  }

  return (
    <div className="trending-news">
      {/* Category Filters */}
      <div className="category-filters">
        {categories.map(cat => (
          <button
            className={selectedCategory === cat ? 'active' : ''}
            onClick={() => setSelectedCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* News Grid */}
      <div className="news-grid">
        {news.map((article, index) => (
          <div className="news-card">
            <img src={article.urlToImage} />
            <h3>{article.title}</h3>
            <p>{article.description}</p>
            <button onClick={() => window.open(article.url, '_blank')}>
              Read More
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
```

**How it works**:
1. Fetches 100 articles from backend
2. Strips HTML tags from titles/descriptions
3. Shuffles articles randomly
4. Shows 12 random articles
5. Each refresh shows different articles

---

### 4. Quick Summary (`frontend/src/components/QuickSummary.jsx`)

**Purpose**: Search and summarize news topics

```jsx
const QuickSummary = () => {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleSummarize = async () => {
    setLoading(true)
    
    // Call backend API
    const response = await api.searchAndSummarize(input)
    
    setResult(response)
    setLoading(false)
  }

  return (
    <div className="quick-summary">
      {/* Input */}
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter a news headline or topic..."
      />
      
      <button onClick={handleSummarize}>
        Summarize with AI
      </button>

      {/* Results */}
      {result && (
        <div>
          {/* AI Summary */}
          <div className="incident-summary">
            <h4>Incident Summary</h4>
            <p>{result.summary}</p>
          </div>

          {/* Related Articles */}
          <div className="related-news">
            <h4>Related News ({result.related_news.length})</h4>
            {result.related_news.map(article => (
              <div className="news-card">
                <h5>{article.title}</h5>
                <p>{article.description}</p>
              </div>
            ))}
          </div>

          {/* Credibility Score */}
          <div className="verification-box">
            <div className="score-circle">
              {result.verification_score}%
            </div>
            <p>{result.verdict}</p>
          </div>
        </div>
      )}
    </div>
  )
}
```

**Backend Flow** (in `api.js`):
```javascript
export const searchAndSummarize = async (headline) => {
  // Step 1: Search for related news
  const searchResponse = await api.post('/agents/news_fetch', {
    query: headline,
    limit: 5
  })
  
  const articles = searchResponse.data.data.articles
  
  // Step 2: Combine article content
  const combinedText = articles.map(a => 
    `${a.title}\n${a.description}`
  ).join('\n\n')
  
  // Step 3: Generate AI summary
  const summaryResponse = await api.post('/agents/summary_context', {
    text: combinedText,
    title: headline
  })
  
  // Step 4: Verify credibility
  const verifyResponse = await api.post('/agents/truth_verification', {
    text: combinedText,
    article_id: 'search_summary'
  })
  
  return {
    summary: summaryResponse.data.data.summary,
    related_news: articles,
    verification_score: verifyResponse.data.data.score,
    verdict: verifyResponse.data.data.verdict
  }
}
```

**Complete Flow**:
```
User enters "AI breakthrough"
    ↓
Search Google News RSS → 5 articles
    ↓
Combine all article text
    ↓
Send to Gemini AI for summary
    ↓
Send to Gemini AI for verification
    ↓
Display:
  - AI-generated summary
  - 5 related articles
  - Credibility score
```

---

### 5. Map Search (`frontend/src/components/MapSearch.jsx`)

**Purpose**: Interactive map for location-based news

```jsx
const MapSearch = () => {
  const [position, setPosition] = useState(null)
  const [keyword, setKeyword] = useState('')
  const [radius, setRadius] = useState(25)
  const [categorizedNews, setCategorizedNews] = useState({})

  const handleLocationSelect = async (latlng) => {
    // Call backend API
    const result = await api.getLocationNews({
      lat: latlng.lat,
      lng: latlng.lng,
      radius_km: radius,
      keyword: keyword
    })
    
    setCategorizedNews(result.categorized_news)
  }

  return (
    <div className="map-search">
      {/* Left: Controls */}
      <div className="map-controls">
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          placeholder="Keyword filter..."
        />
        
        <input
          type="range"
          min="5"
          max="100"
          value={radius}
          onChange={(e) => setRadius(e.target.value)}
        />
      </div>

      {/* Center: Map */}
      <div className="map-container">
        <MapContainer center={position} zoom={12}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <LocationMarker onLocationSelect={handleLocationSelect} />
        </MapContainer>
      </div>

      {/* Right: Categorized News */}
      <div className="news-sidebar">
        {Object.entries(categorizedNews).map(([category, items]) => (
          <div className="news-category">
            <div className="category-header">
              <span>{category === 'Sports' && '⚽'}</span>
              <span>{category} ({items.length})</span>
            </div>
            
            {items.map(news => (
              <div className="news-item">
                <h5>{news.title}</h5>
                <span>{news.distance_km}km away</span>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
```

**How it works**:
1. User clicks map or searches location
2. Gets coordinates (lat, lng)
3. Sends to backend with radius and keyword
4. Backend:
   - Reverse geocodes to location name
   - Searches Google News RSS
   - Filters to last 2 days
   - Categorizes by keywords
5. Frontend displays categorized news in sidebar

---

## API Service Layer (`frontend/src/services/api.js`)

**Purpose**: Centralized API communication

```javascript
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Fetch trending news
export const fetchNews = async (params = {}) => {
  const response = await api.post('/agents/news_fetch', {
    category: params.category || 'all',
    limit: params.limit || 20
  })
  return response.data.data
}

// Analyze text
export const analyzeText = async (text) => {
  // Step 1: Verify
  const verifyResponse = await api.post('/agents/truth_verification', {
    text: text,
    article_id: 'user_input'
  })
  
  // Step 2: Summarize
  const summaryResponse = await api.post('/agents/summary_context', {
    text: text,
    title: 'User Input Analysis'
  })
  
  // Step 3: Impact
  const impactResponse = await api.post('/agents/impact_relevance', {
    text: text,
    context: 'user_analysis'
  })
  
  return {
    verification_score: verifyResponse.data.data.score,
    verdict: verifyResponse.data.data.verdict,
    summary: summaryResponse.data.data.summary,
    impact_score: impactResponse.data.data.impact_score
  }
}

// Get location news
export const getLocationNews = async ({ lat, lng, radius_km, keyword }) => {
  const response = await api.post('/agents/map_intelligence', {
    lat, lng, radius_km, keyword
  })
  
  return {
    news: response.data.data.news,
    categorized_news: response.data.data.categorized_news
  }
}

export default {
  fetchNews,
  analyzeText,
  getLocationNews
}
```

**Why this layer?**
- Centralizes all API calls
- Handles errors consistently
- Makes components cleaner
- Easy to modify API endpoints

---

## Data Flow Examples

### Example 1: Trending News

```
1. User opens app
   ↓
2. TrendingNews component mounts
   ↓
3. useEffect triggers fetchTrendingNews()
   ↓
4. api.fetchNews({ category: 'all', limit: 100 })
   ↓
5. POST http://localhost:8000/agents/news_fetch
   Body: { "category": "all", "limit": 100 }
   ↓
6. Backend: NewsFetchAgent.execute()
   ↓
7. Parse Google News RSS feed
   ↓
8. Return 100 articles
   ↓
9. Frontend: Strip HTML, shuffle, show 12
   ↓
10. Display in grid
```

### Example 2: Quick Summary

```
1. User enters "SpaceX launch"
   ↓
2. Clicks "Summarize with AI"
   ↓
3. api.searchAndSummarize("SpaceX launch")
   ↓
4. POST /agents/news_fetch { query: "SpaceX launch", limit: 5 }
   ↓
5. Backend searches Google News RSS
   ↓
6. Returns 5 articles
   ↓
7. Frontend combines article text
   ↓
8. POST /agents/summary_context { text: combined }
   ↓
9. Backend sends to Gemini AI
   ↓
10. Gemini generates summary
   ↓
11. POST /agents/truth_verification { text: combined }
   ↓
12. Gemini calculates credibility score
   ↓
13. Frontend displays:
    - AI summary
    - 5 related articles
    - Credibility score
```

### Example 3: Location News

```
1. User clicks map at Chennai (13.08, 80.27)
   ↓
2. handleLocationSelect(latlng)
   ↓
3. api.getLocationNews({
     lat: 13.08,
     lng: 80.27,
     radius_km: 25,
     keyword: "sports"
   })
   ↓
4. POST /agents/map_intelligence
   ↓
5. Backend: MapIntelligenceAgent.execute()
   ↓
6. Reverse geocode (13.08, 80.27)
   → "Chennai, India"
   ↓
7. Search Google News RSS for "sports Chennai, India"
   ↓
8. Get 20 articles
   ↓
9. Filter to last 2 days → 13 articles
   ↓
10. Categorize by keywords:
    - Sports: 5 (cricket, ipl, match...)
    - Politics: 3 (government, minister...)
    - Business: 5 (economy, market...)
   ↓
11. Return categorized news
   ↓
12. Frontend displays in sidebar:
    ⚽ Sports (5)
    🏛️ Politics (3)
    💼 Business (5)
```

---

## Key Technologies

### Backend
- **FastAPI**: Modern Python web framework
- **feedparser**: Parse RSS/XML feeds
- **google-generativeai**: Gemini AI SDK
- **requests**: HTTP client
- **uvicorn**: ASGI server

### Frontend
- **React**: UI framework
- **Vite**: Build tool
- **Leaflet.js**: Interactive maps
- **Axios**: HTTP client
- **date-fns**: Date formatting

---

## Configuration

### Backend `.env`
```
GEMINI_API_KEY=your-api-key
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
```

### Frontend `.env`
```
VITE_API_URL=http://localhost:8000
```

---

## Summary

This application demonstrates:

1. **Multi-agent architecture**: Specialized agents for different tasks
2. **AI integration**: Gemini 2.5 Pro for analysis
3. **Free data sources**: Google News RSS (no API key)
4. **Real-time processing**: Async/await for performance
5. **Clean separation**: Frontend/backend architecture
6. **User-friendly**: Interactive maps, category filters, random news

The code is modular, maintainable, and scalable for future enhancements.
