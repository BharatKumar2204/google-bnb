import React, { useState } from 'react'
import { Link as LinkIcon, Send } from 'lucide-react'
import api from '../services/api'
import './UrlAnalysis.css'

const UrlAnalysis = ({ setLoading, setError, setResults }) => {
  const [input, setInput] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim()) {
      setError('Please provide a URL')
      return
    }

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const result = await api.verifyUrl(input)
      setResults(result)
    } catch (error) {
      const errorMessage = error.response?.data?.data?.message || error.message || 'Analysis failed';
      setError(errorMessage);
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="url-analysis">
      <div className="panel-header">
        <LinkIcon size={24} />
        <h3>URL Verification</h3>
        <p>Enter a news article URL to verify its authenticity</p>
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-group">
          <input
            type="url"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="https://example.com/news-article"
            className="url-input"
          />
        </div>

        <button type="submit" className="submit-btn">
          <Send size={20} />
          <span>Analyze with AI</span>
        </button>
      </form>
    </div>
  )
}

export default UrlAnalysis
