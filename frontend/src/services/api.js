import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Trending News API
export const fetchNews = async (params = {}) => {
  try {
    console.log('🔄 Fetching news from backend:', API_BASE_URL)
    const response = await api.post('/agents/news_fetch', {
      category: params.category || 'all',
      limit: params.limit || 20
    })
    console.log('✅ Backend response:', response.data)
    return response.data.data || { articles: [] }
  } catch (error) {
    console.error('❌ Backend error:', error.message)
    console.warn('⚠️ Using mock data - Backend may not be running')
    // Return mock data for demo
    return {
      articles: [
        {
          title: 'Breaking: Major Tech Announcement',
          description: 'A leading tech company announces groundbreaking innovation...',
          url: 'https://example.com/news1',
          urlToImage: 'https://via.placeholder.com/400x200',
          publishedAt: new Date().toISOString(),
          source: { name: 'Tech News' }
        },
        {
          title: 'Global Climate Summit Concludes',
          description: 'World leaders reach historic agreement on climate action...',
          url: 'https://example.com/news2',
          urlToImage: 'https://via.placeholder.com/400x200',
          publishedAt: new Date(Date.now() - 3600000).toISOString(),
          source: { name: 'World News' }
        },
        {
          title: 'AI Breakthrough in Healthcare',
          description: 'New AI system shows promise in early disease detection...',
          url: 'https://example.com/news3',
          urlToImage: 'https://via.placeholder.com/400x200',
          publishedAt: new Date(Date.now() - 7200000).toISOString(),
          source: { name: 'Health Today' }
        }
      ]
    }
  }
}

// Text Analysis
export const analyzeText = async (text) => {
  try {
    console.log('🔄 Analyzing text with AI...')
    
    // First, verify the text
    const verifyResponse = await api.post('/agents/truth_verification', {
      text: text,
      article_id: 'user_input'
    })
    
    console.log('✅ Verification complete:', verifyResponse.data)

    // Then, summarize it
    const summaryResponse = await api.post('/agents/summary_context', {
      text: text,
      title: 'User Input Analysis'
    })
    
    console.log('✅ Summary complete:', summaryResponse.data)

    // Calculate impact
    const impactResponse = await api.post('/agents/impact_relevance', {
      text: text,
      context: 'user_analysis'
    })
    
    console.log('✅ Impact analysis complete:', impactResponse.data)

    const verifyData = verifyResponse.data.data || {}
    const summaryData = summaryResponse.data.data || {}
    const impactData = impactResponse.data.data || {}

    return {
      verification_score: verifyData.score || 75,
      verdict: verifyData.verdict || 'Needs verification',
      summary: summaryData.summary || summaryData.analysis || 'AI analysis completed. The text has been verified for credibility.',
      key_points: summaryData.key_points || ['Analysis complete'],
      impact_score: impactData.impact_score || 60,
      relevance: impactData.relevance || 'Moderate relevance',
      analysis: verifyData.analysis || 'Verification complete'
    }
  } catch (error) {
    console.error('❌ Error analyzing text:', error)
    throw new Error('Failed to analyze text: ' + error.message)
  }
}

// URL Verification
export const verifyUrl = async (url) => {
  try {
    console.log('🔍 Verifying URL:', url)
    
    // Fetch news from URL
    const fetchResponse = await api.post('/agents/news_fetch', {
      url: url
    })

    const fetchData = fetchResponse.data.data || {}
    
    // Check if URL is fake or unreachable
    if (fetchData.is_fake || fetchData.error) {
      console.warn('⚠️ Fake or unreachable URL detected')
      
      // Use AI to analyze the URL itself
      const urlAnalysis = `Analyze this URL for credibility: ${url}\nReason: ${fetchData.reason || fetchData.error}`
      
      const verifyResponse = await api.post('/agents/truth_verification', {
        text: urlAnalysis,
        article_id: url
      })
      
      return {
        verification_score: Math.min(verifyResponse.data.data?.score || 10, 20), // Cap at 20% for fake URLs
        verdict: 'Fake or Unreachable URL',
        summary: `This URL appears to be fake or unreachable. ${fetchData.reason || fetchData.error}`,
        key_points: [
          'URL could not be accessed',
          fetchData.reason || 'Domain may not exist',
          'Likely a test or fake URL'
        ],
        sources: [],
        is_fake: true
      }
    }

    // Verify the content
    const verifyResponse = await api.post('/agents/truth_verification', {
      text: fetchData.content || '',
      article_id: url
    })

    // Summarize
    const summaryResponse = await api.post('/agents/summary_context', {
      text: fetchData.content || '',
      title: fetchData.title || 'Article'
    })

    return {
      verification_score: verifyResponse.data.data?.score || 70,
      verdict: verifyResponse.data.data?.verdict || 'Verification in progress',
      summary: summaryResponse.data.data?.summary || 'Content analyzed',
      key_points: summaryResponse.data.data?.key_points || [],
      sources: verifyResponse.data.data?.sources || []
    }
  } catch (error) {
    console.error('Error verifying URL:', error)
    throw new Error('Failed to verify URL')
  }
}

// Location-based News
export const getLocationNews = async ({ lat, lng, radius_km, keyword }) => {
  try {
    console.log(`🔄 Fetching news for location: ${lat}, ${lng} (${radius_km}km radius)`)
    if (keyword) console.log(`🔍 Keyword filter: ${keyword}`)
    
    const payload = {
      lat: lat,
      lng: lng,
      radius_km: radius_km
    }
    
    if (keyword) {
      payload.keyword = keyword
    }
    
    const response = await api.post('/agents/map_intelligence', payload)
    
    console.log('✅ Location news response:', response.data)

    const data = response.data.data || {}
    const news = data.news || []
    const categorizedNews = data.categorized_news || {}
    
    console.log(`📰 Found ${news.length} news items`)
    console.log(`📂 Categories:`, Object.keys(categorizedNews))

    return {
      news: news,
      categorized_news: categorizedNews,
      location: {
        lat: lat,
        lng: lng,
        area: data.area || 'Selected Area',
        nearby_events: news.length
      },
      summary: data.summary || `Found ${news.length} news items within ${radius_km}km radius`
    }
  } catch (error) {
    console.error('❌ Error fetching location news:', error)
    // Return mock data
    return {
      news: [
        {
          title: 'Local Event Happening Nearby',
          description: 'Community gathering scheduled for this weekend...',
          location: { lat: lat + 0.01, lng: lng + 0.01 }
        },
        {
          title: 'Traffic Update in Your Area',
          description: 'Road construction causing delays on main street...',
          location: { lat: lat - 0.01, lng: lng - 0.01 }
        }
      ],
      categorized_news: {},
      location: {
        lat: lat,
        lng: lng,
        area: 'Selected Location',
        nearby_events: 2
      },
      summary: `Found 2 news items within ${radius_km}km radius`
    }
  }
}

// Verify News (Quick verification)
export const verifyNews = async (text) => {
  try {
    const response = await api.post('/agents/truth_verification', {
      text: text,
      article_id: 'quick_verify'
    })

    return {
      score: response.data.data?.score || 75,
      summary: response.data.data?.verdict || 'Verification complete'
    }
  } catch (error) {
    console.error('Error verifying news:', error)
    return {
      score: 50,
      summary: 'Unable to verify at this time'
    }
  }
}

// Root Agent Query
export const askRootAgent = async (query, context = {}) => {
  try {
    const response = await api.post('/agent/ask', {
      query: query,
      context: context
    })

    return response.data.data || {}
  } catch (error) {
    console.error('Error querying root agent:', error)
    throw new Error('Failed to process query')
  }
}

// Search and Summarize News
export const searchAndSummarize = async (headline) => {
  try {
    console.log('🔍 Searching for news about:', headline)
    
    // Step 1: Search for related news using NewsAPI
    const searchResponse = await api.post('/agents/news_fetch', {
      query: headline,
      limit: 5
    })
    
    const articles = searchResponse.data.data?.articles || []
    console.log(`📰 Found ${articles.length} related articles`)
    
    if (articles.length === 0) {
      return {
        summary: `No recent news articles found about "${headline}". This topic may not have recent coverage or the search terms may need adjustment.`,
        related_news: [],
        verification_score: 50,
        verdict: 'No Data Available'
      }
    }
    
    // Step 2: Combine article content for AI summary
    const combinedText = articles.map(article => 
      `${article.title}\n${article.description || ''}`
    ).join('\n\n')
    
    // Step 3: Generate AI summary using summary agent
    const summaryResponse = await api.post('/agents/summary_context', {
      text: combinedText,
      title: headline
    })
    
    // Step 4: Verify credibility
    const verifyResponse = await api.post('/agents/truth_verification', {
      text: combinedText,
      article_id: 'search_summary'
    })
    
    const summaryData = summaryResponse.data.data || {}
    const verifyData = verifyResponse.data.data || {}
    
    return {
      summary: summaryData.summary || summaryData.analysis || 'Summary generated from related news articles.',
      related_news: articles,
      verification_score: verifyData.score || 70,
      verdict: verifyData.verdict || 'Based on multiple sources',
      key_points: summaryData.key_points || []
    }
  } catch (error) {
    console.error('❌ Error searching and summarizing:', error)
    throw new Error('Failed to search and summarize news: ' + error.message)
  }
}

export default {
  fetchNews,
  analyzeText,
  verifyUrl,
  getLocationNews,
  verifyNews,
  askRootAgent,
  searchAndSummarize
}
