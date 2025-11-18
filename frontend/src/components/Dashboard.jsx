import React, { useState, useEffect } from 'react'
import { 
  Upload, Link as LinkIcon, MapPin, TrendingUp, 
  Search, FileText, CheckCircle, AlertCircle, Loader, Sparkles
} from 'lucide-react'
import TrendingNews from './TrendingNews'
import MapSearch from './MapSearch'
import DeepAnalysis from './DeepAnalysis'
import UrlAnalysis from './UrlAnalysis'
import ResultsPanel from './ResultsPanel'
import MarketRates from './MarketRates'
import './Dashboard.css'

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('trending')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const tabs = [
    { id: 'trending', label: 'Trending News', icon: TrendingUp },
    { id: 'deep-analysis', label: 'Deep Analysis', icon: Sparkles },
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
            <h1>FACT-X</h1>
          </div>
          <p className="tagline">AI-Powered Truth Discovery & News Intelligence</p>
          <MarketRates />
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

          {activeTab === 'deep-analysis' && (
            <>
              <DeepAnalysis
                setLoading={setLoading}
                setError={setError}
                setResults={setResults}
              />
              {results && <ResultsPanel results={results} />}
            </>
          )}

          {activeTab === 'url' && (
            <div className="panel-wrapper">
              <UrlAnalysis
                setLoading={setLoading}
                setError={setError}
                setResults={setResults}
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
