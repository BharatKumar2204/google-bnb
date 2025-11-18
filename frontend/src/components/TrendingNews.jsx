import React, { useState, useEffect } from 'react'
import { TrendingUp, Clock, MapPin, ExternalLink, Loader } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import api from '../services/api'
import './TrendingNews.css'

const TrendingNews = () => {
  const [news, setNews] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState('all')

  const categories = ['all', 'world', 'technology', 'business', 'health', 'science']

  useEffect(() => {
    fetchTrendingNews()
  }, [selectedCategory])

  const fetchTrendingNews = async () => {
    setLoading(true)
    try {
      const response = await api.fetchNews({ category: selectedCategory })
      setNews(response.articles || [])
    } catch (error) {
      console.error('Error fetching news:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleVerify = async (article) => {
    try {
      const result = await api.verifyNews(article.title + ' ' + article.description)
      alert(`Verification Score: ${result.score}/100\n${result.summary}`)
    } catch (error) {
      alert('Verification failed')
    }
  }

  if (loading) {
    return (
      <div className="trending-loading">
        <Loader className="spinner" size={48} />
        <p>Loading trending news...</p>
      </div>
    )
  }

  return (
    <div className="trending-news">
      <div className="trending-header">
        <div className="trending-title">
          <TrendingUp size={28} />
          <h2>Trending News</h2>
        </div>
        <div className="category-filters">
          {categories.map(cat => (
            <button
              key={cat}
              className={`category-btn ${selectedCategory === cat ? 'active' : ''}`}
              onClick={() => setSelectedCategory(cat)}
            >
              {cat.charAt(0).toUpperCase() + cat.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="news-grid">
        {news.map((article, index) => (
          <div key={index} className="news-card">
            {article.urlToImage && (
              <div className="news-image">
                <img src={article.urlToImage} alt={article.title} />
                <div className="news-badge">
                  <TrendingUp size={16} />
                  Trending
                </div>
              </div>
            )}
            
            <div className="news-content">
              <h3 className="news-title">{article.title}</h3>
              <p className="news-description">{article.description}</p>
              
              <div className="news-meta">
                <div className="meta-item">
                  <Clock size={14} />
                  <span>{formatDistanceToNow(new Date(article.publishedAt), { addSuffix: true })}</span>
                </div>
                {article.source && (
                  <div className="meta-item">
                    <span className="source-badge">{article.source.name}</span>
                  </div>
                )}
              </div>

              <div className="news-actions">
                <button 
                  className="btn-verify"
                  onClick={() => handleVerify(article)}
                >
                  Verify
                </button>
                <a 
                  href={article.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="btn-read"
                >
                  <span>Read More</span>
                  <ExternalLink size={16} />
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>

      {news.length === 0 && (
        <div className="no-news">
          <p>No trending news available at the moment</p>
        </div>
      )}
    </div>
  )
}

export default TrendingNews
