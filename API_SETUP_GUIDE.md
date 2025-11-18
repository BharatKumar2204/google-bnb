# 🔑 Complete API Setup Guide

## Table of Contents
1. [Quick Start (No APIs)](#quick-start-no-apis)
2. [NewsAPI Setup](#1-newsapi-setup)
3. [Google Custom Search Setup](#2-google-custom-search-setup)
4. [Google Cloud Platform Setup](#3-google-cloud-platform-setup)
5. [Twitter API Setup](#4-twitter-api-setup-optional)
6. [Reddit API Setup](#5-reddit-api-setup-optional)
7. [Testing Your Setup](#testing-your-setup)

---

## Quick Start (No APIs)

**Good news!** The app works perfectly without any API keys using mock data.

```bash
# 1. Create backend .env
cd ai-news-app/mcp_server
copy .env.example .env

# Edit .env - just keep these:
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
DEBUG=True

# 2. Create frontend .env
cd ../frontend
copy .env.example .env

# Edit .env:
VITE_API_URL=http://localhost:8000

# 3. Run!
cd ..
start-backend.bat  # Terminal 1
start-frontend.bat # Terminal 2
```

✅ **You're done! Open http://localhost:3000**

---

## 1. NewsAPI Setup

Get real trending news from 70,000+ sources worldwide.

### Step 1: Sign Up
1. Go to **https://newsapi.org**
2. Click **"Get API Key"**
3. Fill in:
   - Name: Your name
   - Email: Your email
   - Password: Create password
4. Click **"Submit"**

### Step 2: Get Your API Key
1. After signup, you'll see your API key
2. Copy it (looks like: `abc123def456ghi789jkl012mno345pqr678`)
3. Free tier: 100 requests/day

### Step 3: Add to Backend .env
```env
# In mcp_server/.env
GOOGLE_NEWS_API_KEY=abc123def456ghi789jkl012mno345pqr678
```

### Step 4: Test It
```bash
# Test with curl
curl "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_KEY"
```

### What You Get:
- ✅ Real trending news
- ✅ 70,000+ sources
- ✅ Category filtering
- ✅ 100 requests/day (free)

---

## 2. Google Custom Search Setup

Enable real-time Google search for fact-checking.

### Step 1: Create Google Cloud Project
1. Go to **https://console.cloud.google.com**
2. Click **"Select a project"** → **"New Project"**
3. Enter project name: `news-verification-app`
4. Click **"Create"**
5. Wait for project creation (30 seconds)

### Step 2: Enable Custom Search API
1. In Google Cloud Console, click **"APIs & Services"** → **"Library"**
2. Search for **"Custom Search API"**
3. Click on it
4. Click **"Enable"**
5. Wait for activation

### Step 3: Create API Key
1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"API Key"**
3. Copy your API key (looks like: `AIzaSyD1234567890abcdefghijklmnopqrstuv`)
4. Click **"Restrict Key"** (recommended)
5. Under "API restrictions":
   - Select **"Restrict key"**
   - Check **"Custom Search API"**
6. Click **"Save"**

### Step 4: Create Custom Search Engine
1. Go to **https://programmablesearchengine.google.com/controlpanel/create**
2. Fill in:
   - **Search engine name**: News Verification Search
   - **What to search**: Search the entire web
   - Click **"Create"**
3. Click **"Customize"** → **"Setup"**
4. Copy your **Search engine ID** (looks like: `a1b2c3d4e5f6g7h8i`)

### Step 5: Add to Backend .env
```env
# In mcp_server/.env
GOOGLE_SEARCH_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuv
GOOGLE_SEARCH_ENGINE_ID=a1b2c3d4e5f6g7h8i
```

### Step 6: Test It
```bash
# Test with curl
curl "https://www.googleapis.com/customsearch/v1?key=YOUR_API_KEY&cx=YOUR_ENGINE_ID&q=test"
```

### What You Get:
- ✅ Real Google search results
- ✅ Fact-checking capability
- ✅ Source verification
- ✅ 100 queries/day (free)

---

## 3. Google Cloud Platform Setup

Enable advanced AI features with Vertex AI.

### Step 1: Enable Billing (Required for Vertex AI)
1. In Google Cloud Console, go to **"Billing"**
2. Click **"Link a billing account"**
3. Add credit card (won't be charged without usage)
4. Free tier: $300 credit for 90 days

### Step 2: Enable Vertex AI API
1. Go to **"APIs & Services"** → **"Library"**
2. Search for **"Vertex AI API"**
3. Click **"Enable"**
4. Wait for activation

### Step 3: Enable Other APIs
Enable these for full functionality:
- **Cloud Firestore API** (database)
- **Cloud Storage API** (file storage)

### Step 4: Create Service Account
1. Go to **"IAM & Admin"** → **"Service Accounts"**
2. Click **"Create Service Account"**
3. Fill in:
   - Name: `news-verification-service`
   - Description: `Service account for news verification app`
4. Click **"Create and Continue"**
5. Grant roles:
   - **Vertex AI User**
   - **Cloud Datastore User**
   - **Storage Object Viewer**
6. Click **"Done"**

### Step 5: Create Key
1. Click on your service account
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create new key"**
4. Select **"JSON"**
5. Click **"Create"**
6. Save the downloaded JSON file to:
   ```
   C:\Users\YourName\.config\gcloud\news-verification-credentials.json
   ```

### Step 6: Add to Backend .env
```env
# In mcp_server/.env
GCP_PROJECT_ID=news-verification-app
GCP_REGION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=C:/Users/YourName/.config/gcloud/news-verification-credentials.json

# Vertex AI Models
VERTEX_MODEL_ID=gemini-2.0-flash-exp
VERTEX_VISION_MODEL=gemini-2.0-flash-exp
VERTEX_FLASH_LITE_MODEL=gemini-2.0-flash-exp
```

### Step 7: Test It
```python
# Test in Python
from google.cloud import aiplatform

aiplatform.init(
    project="news-verification-app",
    location="us-central1"
)
print("✅ Vertex AI connected!")
```

### What You Get:
- ✅ Advanced AI analysis
- ✅ Image/video forensics
- ✅ Better summarization
- ✅ Enhanced verification
- ✅ $300 free credit

---

## 4. Twitter API Setup (Optional)

Get real-time tweets for news verification.

### Step 1: Apply for Developer Account
1. Go to **https://developer.twitter.com**
2. Click **"Sign up"** or **"Apply"**
3. Fill in application:
   - Use case: News verification research
   - Will you make Twitter content available: No
   - Will you display tweets: No
4. Wait for approval (can take 1-2 days)

### Step 2: Create App
1. After approval, go to **"Developer Portal"**
2. Click **"Create App"**
3. Fill in:
   - App name: `News Verification App`
   - Description: `AI-powered news verification`
4. Click **"Complete"**

### Step 3: Get Bearer Token
1. Go to your app's **"Keys and tokens"** tab
2. Under **"Bearer Token"**, click **"Generate"**
3. Copy the token (looks like: `AAAAAAAAAAAAAAAAAAAAAA...`)
4. Save it securely

### Step 4: Add to Backend .env
```env
# In mcp_server/.env
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAA...
```

### What You Get:
- ✅ Real-time tweets
- ✅ Trending topics
- ✅ Social media verification
- ✅ 500,000 tweets/month (free)

---

## 5. Reddit API Setup (Optional)

Access Reddit discussions for news context.

### Step 1: Create Reddit App
1. Go to **https://www.reddit.com/prefs/apps**
2. Scroll down and click **"create another app..."**
3. Fill in:
   - Name: `News Verification App`
   - Type: Select **"script"**
   - Description: `AI news verification`
   - About URL: Leave blank
   - Redirect URI: `http://localhost:8000`
4. Click **"create app"**

### Step 2: Get Credentials
1. After creation, you'll see:
   - **Client ID**: Under app name (looks like: `abc123DEF456`)
   - **Client Secret**: Next to "secret" (looks like: `xyz789-ABC123_def456`)
2. Copy both

### Step 3: Add to Backend .env
```env
# In mcp_server/.env
REDDIT_CLIENT_ID=abc123DEF456
REDDIT_CLIENT_SECRET=xyz789-ABC123_def456
```

### What You Get:
- ✅ Reddit discussions
- ✅ Community sentiment
- ✅ Alternative perspectives
- ✅ 60 requests/minute (free)

---

## Complete .env Files

### Backend (.env)
```env
# ============================================
# SERVER CONFIGURATION
# ============================================
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
DEBUG=True

# ============================================
# GOOGLE CLOUD PLATFORM
# ============================================
GCP_PROJECT_ID=news-verification-app
GCP_REGION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=C:/Users/YourName/.config/gcloud/news-verification-credentials.json

# ============================================
# GOOGLE SEARCH API
# ============================================
GOOGLE_SEARCH_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuv
GOOGLE_SEARCH_ENGINE_ID=a1b2c3d4e5f6g7h8i

# ============================================
# NEWS APIS
# ============================================
GOOGLE_NEWS_API_KEY=abc123def456ghi789jkl012mno345pqr678
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAA...
REDDIT_CLIENT_ID=abc123DEF456
REDDIT_CLIENT_SECRET=xyz789-ABC123_def456
GOOGLE_FACT_CHECK_API_KEY=your-fact-check-key

# ============================================
# VERTEX AI MODELS
# ============================================
VERTEX_MODEL_ID=gemini-2.0-flash-exp
VERTEX_VISION_MODEL=gemini-2.0-flash-exp
VERTEX_FLASH_LITE_MODEL=gemini-2.0-flash-exp

# ============================================
# DATABASE
# ============================================
FIRESTORE_DATABASE=news-app-db

# ============================================
# CACHING
# ============================================
CACHE_TTL=300
ENABLE_CACHE=True
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

---

## Testing Your Setup

### Test 1: Backend Health Check
```bash
# Start backend
cd ai-news-app/mcp_server/adk_agent
python main.py

# In another terminal, test:
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "✅ healthy",
  "service": "MCP Server v3.0",
  "root_agent": "Google ADK",
  "agents": ["news_fetch", "truth_verify", "summary", "map_intel", "media_forensics", "impact"]
}
```

### Test 2: News Fetch
```bash
curl -X POST http://localhost:8000/agents/news_fetch \
  -H "Content-Type: application/json" \
  -d '{"category": "technology", "limit": 5}'
```

### Test 3: Google Search
```bash
curl -X POST http://localhost:8000/agent/search \
  -H "Content-Type: application/json" \
  -d '{"query": "latest technology news"}'
```

### Test 4: Text Verification
```bash
curl -X POST http://localhost:8000/agents/truth_verification \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news: Scientists discover new planet", "article_id": "test1"}'
```

### Test 5: Frontend Connection
```bash
# Start frontend
cd ai-news-app/frontend
npm run dev

# Open browser: http://localhost:3000
# Check browser console for errors
```

---

## Troubleshooting

### Issue: "API key not valid"
**Solution:**
- Check key is copied correctly (no spaces)
- Verify API is enabled in Google Cloud Console
- Check billing is enabled (for Vertex AI)

### Issue: "Quota exceeded"
**Solution:**
- Free tiers have limits:
  - NewsAPI: 100 requests/day
  - Google Search: 100 queries/day
- Upgrade to paid tier or wait 24 hours

### Issue: "CORS error"
**Solution:**
- Backend must be running on port 8000
- Frontend must use correct API URL
- Check `VITE_API_URL` in frontend/.env

### Issue: "Module not found"
**Solution:**
```bash
# Backend
cd mcp_server
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

## Cost Breakdown

### Free Tier (Recommended for Development)
- **NewsAPI**: 100 requests/day - FREE
- **Google Search**: 100 queries/day - FREE
- **Google Cloud**: $300 credit for 90 days - FREE
- **Twitter**: 500K tweets/month - FREE
- **Reddit**: 60 requests/minute - FREE

**Total: $0/month** ✅

### Paid Tier (For Production)
- **NewsAPI Pro**: $449/month (unlimited)
- **Google Search**: $5 per 1000 queries
- **Vertex AI**: ~$0.001 per request
- **Twitter**: $100/month (2M tweets)

**Estimated: $50-100/month** for moderate usage

---

## Security Best Practices

### 1. Never Commit .env Files
```bash
# Already in .gitignore
mcp_server/.env
frontend/.env
```

### 2. Use Different Keys for Dev/Prod
```env
# Development
GOOGLE_NEWS_API_KEY=dev_key_here

# Production
GOOGLE_NEWS_API_KEY=prod_key_here
```

### 3. Restrict API Keys
- In Google Cloud Console, restrict keys to specific APIs
- Add IP restrictions for production
- Rotate keys regularly

### 4. Use Environment Variables in Production
```bash
# Don't use .env files in production
# Use system environment variables instead
export GOOGLE_NEWS_API_KEY=your_key
```

---

## Quick Reference

### Get API Keys:
- **NewsAPI**: https://newsapi.org
- **Google Cloud**: https://console.cloud.google.com
- **Twitter**: https://developer.twitter.com
- **Reddit**: https://www.reddit.com/prefs/apps

### Documentation:
- **NewsAPI Docs**: https://newsapi.org/docs
- **Google Search API**: https://developers.google.com/custom-search
- **Vertex AI**: https://cloud.google.com/vertex-ai/docs
- **Twitter API**: https://developer.twitter.com/en/docs
- **Reddit API**: https://www.reddit.com/dev/api

---

## Next Steps

1. ✅ Start with demo mode (no keys needed)
2. ✅ Add NewsAPI for real news
3. ✅ Add Google Search for verification
4. ✅ Add GCP for advanced AI (optional)
5. ✅ Add Twitter/Reddit for social context (optional)

**You're all set!** 🎉

Need help? Check the troubleshooting section or open an issue.
