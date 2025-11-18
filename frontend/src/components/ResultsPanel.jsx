import React from 'react'
import { 
  CheckCircle, XCircle, AlertTriangle, TrendingUp, 
  MapPin, Image, BarChart3, ExternalLink 
} from 'lucide-react'
import './ResultsPanel.css'

const ResultsPanel = ({ results }) => {
  if (!results) return null

  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981'
    if (score >= 60) return '#f59e0b'
    return '#ef4444'
  }

  const getVerificationIcon = (score) => {
    if (score >= 80) return <CheckCircle size={24} color="#10b981" />
    if (score >= 60) return <AlertTriangle size={24} color="#f59e0b" />
    return <XCircle size={24} color="#ef4444" />
  }

  return (
    <div className="results-panel">
      <div className="results-header">
        <h3>Analysis Results</h3>
        <p>Powered by 6 AI Agents</p>
      </div>

      {/* Verification Score */}
      {results.verification_score !== undefined && (
        <div className="score-card">
          <div className="score-header">
            {getVerificationIcon(results.verification_score)}
            <h4>Verification Score</h4>
          </div>
          <div className="score-bar-container">
            <div 
              className="score-bar"
              style={{ 
                width: `${results.verification_score}%`,
                background: getScoreColor(results.verification_score)
              }}
            />
          </div>
          <div className="score-value" style={{ color: getScoreColor(results.verification_score) }}>
            {results.verification_score}/100
          </div>
          {results.verdict && (
            <div className="verdict">
              <strong>Verdict:</strong> {results.verdict}
            </div>
          )}
        </div>
      )}

      {/* Summary */}
      {results.summary && (
        <div className="result-card">
          <div className="card-header">
            <BarChart3 size={20} />
            <h4>Summary</h4>
          </div>
          <p className="card-content">{results.summary}</p>
        </div>
      )}

      {/* Key Points */}
      {results.key_points && results.key_points.length > 0 && (
        <div className="result-card">
          <div className="card-header">
            <CheckCircle size={20} />
            <h4>Key Points</h4>
          </div>
          <ul className="key-points-list">
            {results.key_points.map((point, idx) => (
              <li key={idx}>{point}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Sources */}
      {results.sources && results.sources.length > 0 && (
        <div className="result-card">
          <div className="card-header">
            <ExternalLink size={20} />
            <h4>Sources Verified</h4>
          </div>
          <div className="sources-list">
            {results.sources.map((source, idx) => (
              <a 
                key={idx}
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="source-item"
              >
                <span className="source-name">{source.name}</span>
                <span className="source-reliability">
                  Reliability: {source.reliability || 'N/A'}
                </span>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Location Data */}
      {results.location && (
        <div className="result-card">
          <div className="card-header">
            <MapPin size={20} />
            <h4>Location Information</h4>
          </div>
          <div className="location-info">
            <p><strong>Area:</strong> {results.location.area}</p>
            <p><strong>Coordinates:</strong> {results.location.lat}, {results.location.lng}</p>
            {results.location.nearby_events && (
              <p><strong>Nearby Events:</strong> {results.location.nearby_events}</p>
            )}
          </div>
        </div>
      )}

      {/* Media Analysis */}
      {results.media_analysis && (
        <div className="result-card">
          <div className="card-header">
            <Image size={20} />
            <h4>Media Forensics</h4>
          </div>
          <div className="media-analysis">
            <p><strong>Manipulation Score:</strong> {results.media_analysis.manipulation_score}/100</p>
            <p><strong>Authenticity:</strong> {results.media_analysis.authenticity}</p>
            {results.media_analysis.findings && (
              <p className="findings">{results.media_analysis.findings}</p>
            )}
          </div>
        </div>
      )}

      {/* Impact Score */}
      {results.impact_score !== undefined && (
        <div className="result-card">
          <div className="card-header">
            <TrendingUp size={20} />
            <h4>Impact & Relevance</h4>
          </div>
          <div className="impact-info">
            <div className="impact-score">
              <span>Impact Score:</span>
              <strong>{results.impact_score}/100</strong>
            </div>
            {results.relevance && (
              <p className="relevance">{results.relevance}</p>
            )}
          </div>
        </div>
      )}

      {/* News Articles */}
      {results.news && results.news.length > 0 && (
        <div className="result-card">
          <div className="card-header">
            <TrendingUp size={20} />
            <h4>Related News ({results.news.length})</h4>
          </div>
          <div className="news-list">
            {results.news.map((article, idx) => (
              <div key={idx} className="news-item">
                <h5>{article.title}</h5>
                <p>{article.description}</p>
                {article.url && (
                  <a href={article.url} target="_blank" rel="noopener noreferrer">
                    Read more →
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ResultsPanel
