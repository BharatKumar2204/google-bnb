import { useState } from 'react'
import { Sparkles, Loader } from 'lucide-react'
import api from '../services/api'
import './QuickSummary.css'

const QuickSummary = () => {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSummarize = async () => {
    if (!input.trim()) {
      setError('Please enter a headline or topic')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // Search for related news and generate summary
      const response = await api.searchAndSummarize(input)
      setResult(response)
    } catch (err) {
      setError(err.message || 'Failed to analyze content')
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e) => {
    setInput(e.target.value)
  }

  return (
    <div className="quick-summary">
      <div className="summary-header">
        <Sparkles size={32} />
        <h2>Quick AI Summary</h2>
        <p>Enter a news headline or topic to get related articles and AI-generated summary</p>
      </div>

      <div className="summary-input-section">
        <textarea
          value={input}
          onChange={handleInputChange}
          placeholder="Enter a news headline or topic (e.g., 'AI breakthrough', 'Climate summit', 'SpaceX launch')..."
          className="summary-textarea"
          rows={4}
        />

        <button
          onClick={handleSummarize}
          disabled={loading || !input.trim()}
          className="summarize-btn"
        >
          {loading ? (
            <>
              <Loader size={20} className="spinner" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Sparkles size={20} />
              <span>Summarize with AI</span>
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="summary-error">
          <p>❌ {error}</p>
        </div>
      )}

      {result && (
        <div className="summary-result">
          <div className="result-header">
            <h3>📰 News Summary & Analysis</h3>
          </div>

          {result.summary && (
            <div className="incident-summary">
              <div className="summary-header-box">
                <h4>📝 Incident Summary</h4>
              </div>
              <p className="incident-text">{result.summary}</p>
            </div>
          )}

          {result.related_news && result.related_news.length > 0 && (
            <div className="related-news-section">
              <h4>🔗 Related News Articles ({result.related_news.length})</h4>
              <div className="news-grid">
                {result.related_news.map((article, idx) => (
                  <div key={idx} className="news-card" onClick={() => window.open(article.url, '_blank')}>
                    {article.urlToImage && (
                      <img src={article.urlToImage} alt={article.title} className="news-image" />
                    )}
                    <div className="news-content">
                      <h5 className="news-title">{article.title}</h5>
                      <p className="news-description">{article.description}</p>
                      <div className="news-meta">
                        <span className="news-source">{article.source?.name || 'Unknown'}</span>
                        <span className="news-date">
                          {new Date(article.publishedAt).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {result.verification_score && (
            <div className="verification-box">
              <div className="score-display">
                <div className="score-circle" style={{ '--score': result.verification_score }}>
                  <span className="score-value">{result.verification_score}%</span>
                </div>
                <div className="score-info">
                  <h4>Credibility Score</h4>
                  <p>{result.verdict}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default QuickSummary
