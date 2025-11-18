import React, { useState, useEffect, useRef } from 'react'
import { MapContainer, TileLayer, Marker, Circle, Popup, useMapEvents } from 'react-leaflet'
import { MapPin, Search, Crosshair } from 'lucide-react'
import L from 'leaflet'
import api from '../services/api'
import 'leaflet/dist/leaflet.css'
import './MapSearch.css'

// Fix for default marker icon
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

const LocationMarker = ({ position, setPosition, onLocationSelect }) => {
  useMapEvents({
    click(e) {
      setPosition(e.latlng)
      onLocationSelect(e.latlng)
    },
  })

  return position === null ? null : (
    <>
      <Marker position={position}>
        <Popup>Selected Location</Popup>
      </Marker>
      <Circle
        center={position}
        radius={25000}
        pathOptions={{ color: '#667eea', fillColor: '#667eea', fillOpacity: 0.2 }}
      />
    </>
  )
}

const MapSearch = ({ onResults, setLoading, setError }) => {
  const [position, setPosition] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [keyword, setKeyword] = useState('')
  const [newsMarkers, setNewsMarkers] = useState([])
  const [categorizedNews, setCategorizedNews] = useState({})
  const mapRef = useRef()
  
  const radius = 50 // Fixed radius of 50km

  useEffect(() => {
    // Get user's current location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords
          setPosition({ lat: latitude, lng: longitude })
        },
        () => {
          // Default to a major city if geolocation fails
          setPosition({ lat: 40.7128, lng: -74.0060 }) // New York
        }
      )
    }
  }, [])

  const handleLocationSelect = async (latlng) => {
    setLoading(true)
    setError(null)

    try {
      const result = await api.getLocationNews({
        lat: latlng.lat,
        lng: latlng.lng,
        radius_km: radius,
        keyword: keyword || undefined
      })
      
      console.log('📊 API Result:', result)
      console.log('📰 News count:', result.news?.length)
      console.log('📂 Categorized news:', result.categorized_news)
      
      onResults(result)
      setNewsMarkers(result.news || [])
      setCategorizedNews(result.categorized_news || {})
    } catch (error) {
      setError(error.message || 'Failed to fetch location news')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    setLoading(true)
    try {
      // Geocode the search query
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}`
      )
      const data = await response.json()
      
      if (data && data.length > 0) {
        const { lat, lon } = data[0]
        const newPos = { lat: parseFloat(lat), lng: parseFloat(lon) }
        setPosition(newPos)
        
        if (mapRef.current) {
          mapRef.current.flyTo(newPos, 12)
        }
        
        await handleLocationSelect(newPos)
      } else {
        setError('Location not found')
      }
    } catch (error) {
      setError('Search failed')
    } finally {
      setLoading(false)
    }
  }

  const handleCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords
          const newPos = { lat: latitude, lng: longitude }
          setPosition(newPos)
          
          if (mapRef.current) {
            mapRef.current.flyTo(newPos, 12)
          }
          
          handleLocationSelect(newPos)
        },
        () => {
          setError('Unable to get current location')
        }
      )
    }
  }

  if (!position) {
    return (
      <div className="map-loading">
        <MapPin size={48} />
        <p>Loading map...</p>
      </div>
    )
  }

  return (
    <div className="map-search">
      <div className="map-controls">
        <div className="control-header">
          <MapPin size={24} />
          <h3>Location-Based News</h3>
          <p>Click on the map or search for a location to find local news</p>
        </div>

        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search for a location..."
            className="search-input"
          />
          <button type="submit" className="search-btn">
            <Search size={20} />
          </button>
        </form>

        <div className="keyword-control">
          <label>Keyword Filter:</label>
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="e.g., Chennai, Sports..."
            className="keyword-input"
          />
        </div>

        <button onClick={handleCurrentLocation} className="current-location-btn">
          <Crosshair size={20} />
          <span>Use Current Location</span>
        </button>
      </div>

      <div className="map-container">
        <MapContainer
          center={position}
          zoom={12}
          style={{ height: '100%', width: '100%' }}
          ref={mapRef}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <LocationMarker
            position={position}
            setPosition={setPosition}
            onLocationSelect={handleLocationSelect}
          />
        </MapContainer>
      </div>

      <div className="news-sidebar">
        <h4>
          📰 Local News ({newsMarkers.length}) - Last 2 Days
        </h4>
        
        {Object.keys(categorizedNews).length > 0 ? (
          <div className="categorized-news">
            {Object.entries(categorizedNews).map(([category, items]) => (
              <div key={category} className="news-category">
                <div className="category-header">
                  <span className="category-icon">
                    {category === 'Sports' && '⚽'}
                    {category === 'Politics' && '🏛️'}
                    {category === 'Business' && '💼'}
                    {category === 'Technology' && '💻'}
                    {category === 'Entertainment' && '🎬'}
                    {category === 'Health' && '🏥'}
                    {category === 'Science' && '🔬'}
                    {category === 'Other' && '📰'}
                  </span>
                  <span className="category-name">{category}</span>
                  <span className="category-count">({items.length})</span>
                </div>
                <div className="news-list">
                  {items.map((news, idx) => (
                    <div 
                      key={idx} 
                      className="news-item"
                      onClick={() => window.open(news.url, '_blank')}
                    >
                      <div className="news-item-title">
                        {news.title}
                      </div>
                      <div className="news-item-meta">
                        <span>{news.distance_km}km away</span>
                        <span className="news-item-source">
                          {news.source || news.source_type}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-news">
            Click on the map to find local news
          </div>
        )}
      </div>
    </div>
  )
}

export default MapSearch
