import React, { useState, useEffect } from 'react'
import api from '../services/api'
import { DollarSign, RefreshCw } from 'lucide-react'
import './MarketRates.css'

const MarketRates = () => {
  const [goldPrice, setGoldPrice] = useState(null)
  const [silverPrice, setSilverPrice] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchMarketRates = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await api.fetchMetalPrices()
      if (response.gold && response.silver) {
        setGoldPrice(response.gold.price)
        setSilverPrice(response.silver.price)
      } else {
        setError("Could not fetch gold and silver prices.")
      }
    } catch (err) {
      console.error("Error fetching market rates:", err)
      setError("Failed to load market rates.")
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchMarketRates()
    const interval = setInterval(fetchMarketRates, 300000); // Refresh every 5 minutes
    return () => clearInterval(interval);
  }, [])

  if (loading) {
    return (
      <div className="market-rates loading">
        <DollarSign size={20} className="spinner" />
        <span>Loading...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div className="market-rates error">
        <span>{error}</span>
        <button onClick={fetchMarketRates} className="refresh-btn">
          <RefreshCw size={16} />
        </button>
      </div>
    )
  }

  return (
    <div className="market-rates">
      <div className="rate-item gold">
        <span className="label">Gold:</span>
        <span className="price">${goldPrice ? goldPrice.toFixed(2) : 'N/A'}</span>
      </div>
      <div className="rate-item silver">
        <span className="label">Silver:</span>
        <span className="price">${silverPrice ? silverPrice.toFixed(2) : 'N/A'}</span>
      </div>
      <button onClick={fetchMarketRates} className="refresh-btn">
        <RefreshCw size={16} />
      </button>
    </div>
  )
}

export default MarketRates