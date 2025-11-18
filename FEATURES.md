# FACT-X - Feature Documentation

## Recent Enhancements

This document consolidates all recent feature improvements to the FACT-X news verification platform.

---

## 1. Deep Analysis with Smart Keyword Extraction

### Overview
Enhanced Deep Analysis feature with AI-powered keyword extraction and intelligent news search.

### Key Features
- **AI-Powered Keywords**: Uses Gemini 2.5 Pro to extract meaningful search terms
- **Multi-Keyword Search**: Searches with top 3 keywords instead of single words
- **Ad Filtering**: Automatically removes sponsored content
- **Comprehensive Results**: Returns up to 10 relevant articles

### Example
```
Input: "Tesla announces new AI chip"
Keywords Extracted: ["Tesla", "announces", "chip"]
Search: Uses all 3 keywords for better results
```

**Documentation**: See `DEEP_ANALYSIS_IMPROVEMENTS.md` for details

---

## 2. Dynamic Verification Scoring

### Overview
Replaced static 75/100 scores with dynamic scoring based on actual sources found.

### Scoring Formula

#### Base Score (by source count)
- 1 source = 5%
- 2 sources = 10%
- 3 sources = 15%
- ...
- 10+ sources = 40%

#### Quality Bonus
- High-reliability sources: +15 points each (Reuters, BBC, NYT, etc.)
- Medium-reliability sources: +8 points each (CNN, Fox News, etc.)

### Score Ranges
- **80-100**: Highly Credible - Multiple Reliable Sources
- **60-79**: Credible - Multiple Sources Found
- **40-59**: Moderately Credible - Limited Sources
- **20-39**: Low Credibility - Few Sources
- **0-19**: Unverifiable - Insufficient Sources

### Visual Features
- Color-coded scores (green/yellow/red)
- Real-time verification in Trending News
- Source breakdown display
- Loading states during verification

**Documentation**: See `DYNAMIC_VERIFICATION_SCORING.md` for details

---

## 3. Fake News Detection System

### Overview
3-layer system to detect and filter fake news, satire, and misleading headlines.

### Layer 1: AI Absurdity Detection
Detects obviously fake claims:
- Physical impossibility
- Satirical content
- Obvious contradictions
- Extraordinary claims

**Example:**
```
"Scientists Confirm Cats Are Now Eligible for Tax Returns"
→ Detected as absurd
→ Score: 5/100
→ Verdict: "Likely Fake/Satirical"
```

### Layer 2: Relevance Filtering
Ensures search results match the headline:
- Calculates relevance score (0-100%)
- Filters articles below 30% relevance
- Prevents keyword-only matches

**Example:**
```
Headline: "Cats eligible for tax returns"
Found: 10 generic cat articles
Relevance: 0% (no mention of tax returns)
Result: Filtered out, Score: 5/100
```

### Layer 3: No Relevant Sources Detection
If search finds articles but none are relevant:
- Score: 5/100
- Clear message about lack of relevant sources
- Prevents false positives

**Documentation**: See `FAKE_NEWS_DETECTION.md` for details

---

## 4. Advertisement Filtering

### Overview
Automatically filters out sponsored content and advertisements from all news sections.

### Detection Patterns
- Direct indicators: "sponsored", "promoted", "[ad]"
- Shopping language: "buy now", "sale", "discount"
- Marketing phrases: "click here", "sign up", "free trial"
- Product launches and affiliate content

### Applied To
- Trending News
- Deep Analysis results
- Location-based news
- All search results

### Impact
- Cleaner news feeds
- More accurate source counts
- Better credibility scores
- Improved user trust

---

## 5. Enhanced UI/UX

### Trending News
- Dynamic verification scores (not static 75/100)
- Click "Verify" to see real-time score
- Color-coded score display
- Loading states during verification
- Detailed source breakdown in alerts

### Deep Analysis
- Shows keywords used in search
- Source quality breakdown with badges
- High-quality sources highlighted in green
- Medium-quality sources highlighted in blue
- Relevance-based article filtering

### Results Panel
- Source analysis details
- Keyword tags display
- Color-coded credibility indicators
- Comprehensive breakdown of findings

---

## Technical Stack

### Backend
- **Python 3.11** with FastAPI
- **Gemini 2.5 Pro** for AI analysis
- **Google News RSS** for news search (free, no API key)
- **OpenStreetMap** for location services

### Frontend
- **React 18** with Vite
- **Leaflet.js** for maps
- **Axios** for API calls
- **date-fns** for date formatting

### AI Capabilities
- Keyword extraction
- Absurdity detection
- Content summarization
- Relevance scoring
- Credibility analysis

---

## Configuration

### Environment Variables
```env
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional
GOOGLE_SEARCH_API_KEY=your_search_key
GOOGLE_SEARCH_ENGINE_ID=your_engine_id
```

### Adjustable Parameters
- **Relevance Threshold**: Default 30% (in `deep_analysis_agent.py`)
- **Source Limits**: Default 10-15 articles per search
- **Cache Duration**: Configurable in news fetch agent

---

## Performance Metrics

### Response Times
- Absurdity detection: ~1-2 seconds (AI call)
- Relevance filtering: <100ms (local computation)
- News search: ~1-3 seconds (RSS parsing)
- Total verification: ~2-5 seconds

### Accuracy Improvements
- **Before**: 55/100 for fake news (keyword matches)
- **After**: 5/100 for fake news (properly detected)
- **Reduction in false positives**: ~90%

---

## Future Roadmap

### Planned Features
1. **Fact-Checking APIs**: Integration with Snopes, FactCheck.org
2. **Historical Tracking**: Monitor source reliability over time
3. **Social Media Signals**: Check viral status on social platforms
4. **Image Verification**: Reverse image search for manipulated photos
5. **Domain Reputation**: Blacklist known fake news sites
6. **User Feedback**: Allow users to report inaccurate scores
7. **Caching System**: Store verification results to reduce API calls
8. **Multi-Language Support**: Analyze news in multiple languages

### Optimization Goals
- Reduce verification time to <1 second
- Increase accuracy to 95%+
- Add more high-reliability sources
- Implement machine learning for pattern detection

---

## Support & Documentation

### Main Documentation
- **README.md**: Complete setup and usage guide
- **DEEP_ANALYSIS_IMPROVEMENTS.md**: Deep analysis feature details
- **DYNAMIC_VERIFICATION_SCORING.md**: Scoring system documentation
- **FAKE_NEWS_DETECTION.md**: Fake news detection system

### Getting Help
- Check the README.md for setup instructions
- Review feature documentation for specific capabilities
- Check logs for debugging information
- Ensure all environment variables are set correctly

---

**Last Updated**: November 2024
**Version**: 3.0
**Platform**: FACT-X - AI-Powered Truth Discovery & News Intelligence
