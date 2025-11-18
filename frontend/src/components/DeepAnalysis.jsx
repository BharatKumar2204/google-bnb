import { useState } from 'react'
import { Sparkles, Loader, Send } from 'lucide-react'
import api from '../services/api'
import './DeepAnalysis.css'
import ResultsPanel from './ResultsPanel'

const DeepAnalysis = ({ setLoading, setError, setResults }) => {
  const [input, setInput] = useState('')

  const handleAnalyze = async () => {
    if (!input.trim()) {
      setError('Please enter a headline, topic, or text to analyze.')
      return
    }

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      let response
      // If input is short, treat as a query to search for news
      if (input.length < 150) {
        response = await api.searchAndSummarize(input)
      } else {
        // If input is long, treat as text to be analyzed
        response = await api.analyzeText(input)
      }
      setResults(response)
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
    <div className="deep-analysis">
      <div className="analysis-header">
        <Sparkles size={32} />
        <h2>Deep Analysis</h2>
        <p>Enter a news headline, topic, or paste any text for a deep AI-powered analysis.</p>
      </div>

      <div className="analysis-input-section">
        <textarea
          value={input}
          onChange={handleInputChange}
          placeholder="Enter a news headline, topic, or paste text here..."
          className="analysis-textarea"
          rows={6}
        />

        <button
          onClick={handleAnalyze}
          disabled={!input.trim()}
          className="analyze-btn"
        >
          <Send size={20} />
          <span>Analyze with AI</span>
        </button>
      </div>
    </div>
  )
}

export default DeepAnalysis
