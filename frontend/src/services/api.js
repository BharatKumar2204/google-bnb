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
    console.error('❌ Backend error:', error.message);
    throw error;
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
    console.error('❌ Error fetching location news:', error);
    throw error;
  }
}

// Verify News (Quick verification with source-based scoring)
export const verifyNews = async (text) => {
  try {
    console.log('🔍 Quick verification for:', text.substring(0, 50) + '...')
    
    // Use deep analysis for better verification
    const response = await api.post('/agents/deep_analysis', {
      headline: text
    })

    const data = response.data.data || {}
    
    console.log(`✅ Verification: ${data.verification_score}/100 (${data.source_analysis?.source_count || 0} sources)`)

    return {
      score: data.verification_score || 50,
      summary: data.verdict || 'Verification complete',
      sources: data.source_analysis?.source_count || 0,
      details: data.source_analysis?.reason || ''
    }
  } catch (error) {
    console.error('Error verifying news:', error)
    return {
      score: 50,
      summary: 'Unable to verify at this time',
      sources: 0
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

// Search and Summarize News - Enhanced with Deep Analysis
export const searchAndSummarize = async (headline) => {
  try {
    console.log('🔍 Deep Analysis for:', headline)
    
    // Use the new Deep Analysis agent
    const response = await api.post('/agents/deep_analysis', {
      headline: headline
    })
    
    const data = response.data.data || {}
    
    console.log(`✅ Deep Analysis complete:`)
    console.log(`   Score: ${data.verification_score}/100`)
    console.log(`   Sources: ${data.source_analysis?.source_count || 0}`)
    console.log(`   Keywords: ${data.keywords_used?.join(', ')}`)
    
    return {
      summary: data.summary || 'Analysis complete',
      related_news: data.related_news || [],
      verification_score: data.verification_score || 50,
      verdict: data.verdict || 'Analysis complete',
      key_points: data.key_points || [],
      source_analysis: data.source_analysis || {},
      keywords_used: data.keywords_used || []
    }
  } catch (error) {
    console.error('❌ Error in deep analysis:', error)
    throw new Error('Failed to analyze news: ' + error.message)
  }
}

// Fetch Metal Prices
export const fetchMetalPrices = async () => {
  try {
    console.log('💰 Fetching metal prices...')
    const response = await api.get('/agents/metal_prices')
    console.log('✅ Metal prices response:', response.data)
    return response.data.data || { gold: null, silver: null }
  } catch (error) {
    console.error('❌ Error fetching metal prices:', error)
    throw error
  }
}

export default {
  fetchNews,
  analyzeText,
  verifyUrl,
  getLocationNews,
  verifyNews,
  askRootAgent,
  searchAndSummarize,
  fetchMetalPrices
}
