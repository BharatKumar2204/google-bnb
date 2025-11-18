"""
Agent for fetching real-time gold and silver prices.
Uses APILayer's Gold & Silver Price API (or similar).
"""

import logging
import requests
from typing import Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MetalPricesAgent:
    def __init__(self, config, gcp_clients):
        self.config = config
        self.gcp_clients = gcp_clients
        self.logger = logging.getLogger("agent.metal_prices")
        self.api_key = self.config.APILAYER_API_KEY # This is now metalpriceapi.com key
        self.base_url = "https://api.metalpriceapi.com/v1/latest?base=inr" # New API endpoint
        self.cache = {}
        self.cache_expiry_time = timedelta(minutes=10) # Cache for 10 minutes

    async def execute(self, payload: Dict) -> Dict:
        """Fetch gold and silver prices."""
        try:
            if not self.api_key:
                self.logger.warning("⚠️ METALPRICEAPI_API_KEY not found, returning mock data.")
                return self._get_mock_prices()

            cache_key = "metal_prices_latest"
            if cache_key in self.cache and datetime.now() < self.cache[cache_key]["expiry"]:
                self.logger.info("✅ Serving metal prices from cache.")
                return self.cache[cache_key]["data"]

            self.logger.info("💰 Fetching real-time gold and silver prices from MetalPriceAPI.")
            
            # API key is passed as a query parameter
            params = {
                "api_key": self.api_key,
                "base": "INR", # Assuming base currency is USD
                "currencies": "XAU,XAG" # Global Gold and Silver
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status() # Raise an exception for HTTP errors

            data = response.json()
            
            # Expected response structure from metalpriceapi.com:
            # {
            #   "success": true,
            #   "timestamp": 1678886400,
            #   "date": "2023-03-15",
            #   "base": "USD",
            #   "rates": {
            #     "XAU": 1900.00,
            #     "XAG": 22.00
            #   }
            # }
            
            gold_price = data.get("rates", {}).get("XAU")
            silver_price = data.get("rates", {}).get("XAG")
            currency = data.get("base", "USD") # Base currency from API response

            if gold_price is None or silver_price is None:
                self.logger.error(f"Failed to parse gold/silver prices from API response: {data}")
                return self._get_mock_prices()

            result = {
                "gold": {"price": gold_price, "currency": currency},
                "silver": {"price": silver_price, "currency": currency},
                "timestamp": datetime.now().isoformat(),
                "source": "metalpriceapi.com"
            }
            
            self.cache[cache_key] = {
                "data": result,
                "expiry": datetime.now() + self.cache_expiry_time
            }
            
            self.logger.info("✅ Successfully fetched metal prices.")
            return result

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching metal prices from API: {e}")
            return self._get_mock_prices()
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return self._get_mock_prices()

    def _get_mock_prices(self) -> Dict:
        """Returns mock gold and silver prices for development/error fallback."""
        self.logger.info("Returning mock metal prices.")
        return {
            "gold": {"price": 1950.00, "currency": "USD"},
            "silver": {"price": 23.50, "currency": "USD"},
            "timestamp": datetime.now().isoformat(),
            "source": "mock_data"
        }
