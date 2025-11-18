import React, { useState, useEffect } from 'react'
import { 
  Upload, Link as LinkIcon, MapPin, TrendingUp, 
  Search, FileText, CheckCircle, AlertCircle, Loader, Sparkles
} from 'lucide-react'
import TrendingNews from './TrendingNews'
import MapSearch from './MapSearch'
import InputPanel from './InputPanel'
import ResultsPanel from './ResultsPanel'
import QuickSummary from './QuickSummary'
import './Dashboard.css'

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('trending')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const tabs = [
    { id: 'trending', label: 'Trending News', icon: TrendingUp },
    { id: 'summary', label: 'Quick Summary', icon: Sparkles },
    { id: 'text', label: 'Text Analysis', icon: FileText },
    { id: 'url', label: 'URL Verification', icon: LinkIcon },
    { id: 'map', label: 'Location News', icon: MapPin }
  ]

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="logo">
            <CheckCircle size={32} />
            <h1>AI News Verification</h1>
          </div>
          <p className="tagline">Real-time news verification powered by AI</p>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="dashboard-nav">
        <div className="nav-container">
          {tabs.map(tab => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => {
                  setActiveTab(tab.id)
                  setResults(null)
                  setError(null)
                }}
              >
                <Icon size={20} />
                <span>{tab.label}</span>
              </button>
            )
          })}
        </div>
      </nav>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="content-container">
          {activeTab === 'trending' && (
            <TrendingNews />
          )}

          {activeTab === 'summary' && (
            <QuickSummary />
          )}

          {activeTab === 'text' && (
            <div className="panel-wrapper">
              <InputPanel
                type="text"
                onSubmit={setResults}
                setLoading={setLoading}
                setError={setError}
              />
              {results && <ResultsPanel results={results} />}
            </div>
          )}

          {activeTab === 'url' && (
            <div className="panel-wrapper">
              <InputPanel
                type="url"
                onSubmit={setResults}
                setLoading={setLoading}
                setError={setError}
              />
              {results && <ResultsPanel results={results} />}
            </div>
          )}

          {activeTab === 'map' && (
            <MapSearch
              onResults={setResults}
              setLoading={setLoading}
              setError={setError}
            />
          )}

          {/* Loading State */}
          {loading && (
            <div className="loading-overlay">
              <Loader className="spinner" size={48} />
              <p>Analyzing with AI agents...</p>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="error-banner">
              <AlertCircle size={20} />
              <span>{error}</span>
              <button onClick={() => setError(null)}>×</button>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>Powered by Google ADK • 6 Specialized AI Agents • Real-time Verification</p>
      </footer>
    </div>
  )
}

export default Dashboard
