# API Keys Setup Guide

## Required API Keys

### 1. Google Gemini API Key (REQUIRED)

This is the only required API key for the application to work.

**How to get it:**

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key
5. Paste it in `mcp_server/.env`:
   ```
   GEMINI_API_KEY=AIzaSy...your-key-here
   ```

**What it's used for:**
- News verification (credibility scoring)
- Text summarization
- Content analysis
- Impact assessment

---

## Optional API Keys

### 2. Google Search API (OPTIONAL)

Enhances fact-checking by cross-referencing with search results.

**How to get it:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Custom Search API"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the API key
6. Create a Custom Search Engine at [Programmable Search Engine](https://programmablesearchengine.google.com/)
7. Get your Search Engine ID
8. Add to `mcp_server/.env`:
   ```
   GOOGLE_SEARCH_API_KEY=AIzaSy...your-key-here
   GOOGLE_SEARCH_ENGINE_ID=your-engine-id-here
   ```

**What it's used for:**
- Enhanced fact-checking
- Cross-referencing claims
- Finding related sources

---

### 3. NewsAPI Key (NOT REQUIRED)

The app uses free Google News RSS, so this is not needed.

**If you want to use it anyway:**

1. Go to [NewsAPI.org](https://newsapi.org/)
2. Sign up for free account
3. Get your API key
4. Add to `mcp_server/.env`:
   ```
   NEWS_API_KEY=your-newsapi-key-here
   ```

**Note:** Free tier has 100 requests/day limit. Google News RSS is unlimited and free.

---

### 4. Google Cloud Credentials (OPTIONAL)

Only needed if you want to use GCP services like Firestore.

**How to set up:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project
3. Enable required APIs (Firestore, etc.)
4. Go to "IAM & Admin" → "Service Accounts"
5. Create service account
6. Download JSON key file
7. Save as `mcp_server/credentials.json`
8. Add to `mcp_server/.env`:
   ```
   GCP_PROJECT_ID=your-project-id
   GOOGLE_APPLICATION_CREDENTIALS=credentials.json
   ```

**What it's used for:**
- Firestore database (optional)
- Cloud Storage (optional)
- Other GCP services (optional)

---

## Configuration File Location

All API keys go in: `ai-news-app/mcp_server/.env`

**Example `.env` file:**

```env
# Required
GEMINI_API_KEY=AIzaSyDgOPQPtuCgmA62H-IfuhPp07f9FN5Y74Y

# Optional
GOOGLE_SEARCH_API_KEY=AIzaSyDgOPQPtuCgmA62H-IfuhPp07f9FN5Y74Y
GOOGLE_SEARCH_ENGINE_ID=017576662512468239146:omuauf_lfve

# Server
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
```

---

## What Works Without API Keys?

**With only Gemini API key:**
- ✅ Trending News (uses free Google News RSS)
- ✅ Quick Summary (uses Gemini AI)
- ✅ Text Analysis (uses Gemini AI)
- ✅ Location News (uses free Google News RSS + Gemini AI)
- ✅ News verification
- ✅ Summarization
- ✅ Categorization

**Without Gemini API key:**
- ❌ Verification won't work
- ❌ Summarization won't work
- ❌ AI analysis won't work
- ✅ News fetching still works (Google News RSS)

---

## Testing Your Setup

After adding your Gemini API key:

1. Start the backend:
   ```bash
   cd ai-news-app/mcp_server
   python run_server.py
   ```

2. Check the logs for:
   ```
   ✅ Gemini 2.5 Pro enabled for verification
   ```

3. Test the API:
   ```bash
   curl http://localhost:8000/health
   ```

4. You should see:
   ```json
   {
     "status": "✅ healthy",
     "service": "MCP Server v3.0"
   }
   ```

---

## Troubleshooting

**"Gemini AI not available"**
- Check that GEMINI_API_KEY is set in `.env`
- Verify the API key is valid
- Make sure there are no quotes around the key

**"No NewsAPI key found"**
- This is just a warning, not an error
- The app will use Google News RSS instead
- You can ignore this message

**"GCP init skipped"**
- This is normal if you're not using GCP services
- The app will work fine without it

---

## Cost Information

**Free:**
- Google News RSS (unlimited)
- OpenStreetMap Nominatim (geocoding)

**Paid (but has free tier):**
- Gemini API: Free tier available
- Google Search API: 100 queries/day free
- NewsAPI: 100 requests/day free

**Recommended for this project:**
- Just use Gemini API (free tier is generous)
- Skip NewsAPI (use Google News RSS instead)
- Skip Google Search API (optional enhancement)

---

## Security Notes

**Important:**
- Never commit `.env` file to Git
- Never share your API keys
- Add `.env` to `.gitignore`
- Rotate keys if accidentally exposed

**The `.env` file is already in `.gitignore`** ✅

---

## Quick Start

Minimum setup to run the app:

1. Get Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create `mcp_server/.env`:
   ```env
   GEMINI_API_KEY=your-key-here
   MCP_SERVER_HOST=localhost
   MCP_SERVER_PORT=8000
   ```
3. Start backend: `python run_server.py`
4. Start frontend: `npm run dev`
5. Done! 🎉

---

For more help, check the main README.md file.
