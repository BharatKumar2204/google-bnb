import React, { useState } from 'react'
import { Upload, Link as LinkIcon, Send, FileText } from 'lucide-react'
import api from '../services/api'
import './InputPanel.css'

const InputPanel = ({ type, onSubmit, setLoading, setError }) => {
  const [input, setInput] = useState('')
  const [file, setFile] = useState(null)

  const handleFileUpload = (e) => {
    const uploadedFile = e.target.files[0]
    if (uploadedFile) {
      setFile(uploadedFile)
      const reader = new FileReader()
      reader.onload = (event) => {
        setInput(event.target.result)
      }
      reader.readAsText(uploadedFile)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim()) {
      setError('Please provide input')
      return
    }

    setLoading(true)
    setError(null)

    try {
      let result
      if (type === 'text') {
        result = await api.analyzeText(input)
      } else if (type === 'url') {
        result = await api.verifyUrl(input)
      }
      onSubmit(result)
    } catch (error) {
      const errorMessage = error.response?.data?.data?.message || error.message || 'Analysis failed';
      setError(errorMessage);
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="input-panel">
      <div className="panel-header">
        {type === 'text' ? (
          <>
            <FileText size={24} />
            <h3>Text Analysis</h3>
            <p>Upload WhatsApp chat or paste text for verification</p>
          </>
        ) : (
          <>
            <LinkIcon size={24} />
            <h3>URL Verification</h3>
            <p>Enter a news article URL to verify its authenticity</p>
          </>
        )}
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        {type === 'text' && (
          <div className="file-upload">
            <input
              type="file"
              id="file-input"
              accept=".txt,.csv"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
            <label htmlFor="file-input" className="upload-btn">
              <Upload size={20} />
              <span>Upload WhatsApp Chat</span>
            </label>
            {file && (
              <span className="file-name">
                {file.name}
              </span>
            )}
          </div>
        )}

        <div className="input-group">
          {type === 'text' ? (
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Paste WhatsApp messages or any text to analyze..."
              rows={10}
              className="text-input"
            />
          ) : (
            <input
              type="url"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="https://example.com/news-article"
              className="url-input"
            />
          )}
        </div>

        <button type="submit" className="submit-btn">
          <Send size={20} />
          <span>Analyze with AI</span>
        </button>
      </form>
    </div>
  )
}

export default InputPanel
