"""
Weather Service for OpenWeatherMap API Integration
Handles API calls, data parsing, caching, and error handling
"""

import requests
from datetime import datetime, timedelta
from django.conf import settings
from typing import Dict, List, Optional


class WeatherService:
    """
    Service class for interacting with OpenWeatherMap API
    """
    
    # Reinach BL, Switzerland coordinates
    REINACH_LAT = 47.4953
    REINACH_LON = 7.5965
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        # Simple in-memory cache
        self._cache = {}
        self._cache_duration = timedelta(minutes=10)
    
    def get_current_weather(self, location: str = None) -> Optional[Dict]:
        """
        Get current weather data for Reinach BL
        
        Args:
            location: Not used, defaults to Reinach BL
            
        Returns:
            Dictionary with current weather data or None if error
        """
        cache_key = "current_weather"
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]['data']
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': self.REINACH_LAT,
                'lon': self.REINACH_LON,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            parsed_data = self._parse_current_weather(data)
            
            # Cache the result
            self._update_cache(cache_key, parsed_data)
            
            return parsed_data
            
        except requests.exceptions.RequestException as e:
            return self._handle_api_error(e)
    
    def get_forecast_24h(self, location: str = None) -> Optional[List[Dict]]:
        """
        Get 24-hour forecast for Reinach BL
        
        Args:
            location: Not used, defaults to Reinach BL
            
        Returns:
            List of forecast data dictionaries or None if error
        """
        cache_key = "forecast_24h"
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]['data']
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': self.REINACH_LAT,
                'lon': self.REINACH_LON,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': 8  # 8 x 3-hour intervals = 24 hours
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            parsed_data = self._parse_forecast(data)
            
            # Cache the result
            self._update_cache(cache_key, parsed_data)
            
            return parsed_data
            
        except requests.exceptions.RequestException as e:
            return self._handle_api_error(e)
    
    def _parse_current_weather(self, data: Dict) -> Dict:
        """
        Parse current weather API response
        
        Args:
            data: Raw API response
            
        Returns:
            Parsed weather data
        """
        return {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'] * 3.6,  # Convert m/s to km/h
            'precipitation': data.get('rain', {}).get('1h', 0),  # mm in last hour
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'timestamp': datetime.fromtimestamp(data['dt']),
            'location': f"{data['name']}, {data['sys']['country']}"
        }
    
    def _parse_forecast(self, data: Dict) -> List[Dict]:
        """
        Parse forecast API response
        
        Args:
            data: Raw API response
            
        Returns:
            List of parsed forecast data
        """
        forecasts = []
        
        for item in data['list']:
            forecast = {
                'timestamp': datetime.fromtimestamp(item['dt']),
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'] * 3.6,  # Convert m/s to km/h
                'precipitation': item.get('rain', {}).get('3h', 0),  # mm in 3 hours
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon']
            }
            forecasts.append(forecast)
        
        return forecasts
    
    def _handle_api_error(self, error: Exception) -> None:
        """
        Handle API errors and return appropriate response
        
        Args:
            error: The exception that occurred
            
        Returns:
            None to indicate error
        """
        if isinstance(error, requests.exceptions.Timeout):
            print(f"API timeout error: {error}")
        elif isinstance(error, requests.exceptions.HTTPError):
            if error.response.status_code == 401:
                print("Invalid API key")
            elif error.response.status_code == 429:
                print("API rate limit exceeded")
            else:
                print(f"HTTP error: {error.response.status_code}")
        else:
            print(f"API request failed: {error}")
        
        return None
    
    def _is_cache_valid(self, key: str) -> bool:
        """
        Check if cached data is still valid
        
        Args:
            key: Cache key
            
        Returns:
            True if cache is valid, False otherwise
        """
        if key not in self._cache:
            return False
        
        cached_time = self._cache[key]['timestamp']
        return datetime.now() - cached_time < self._cache_duration
    
    def _update_cache(self, key: str, data: any) -> None:
        """
        Update cache with new data
        
        Args:
            key: Cache key
            data: Data to cache
        """
        self._cache[key] = {
            'data': data,
            'timestamp': datetime.now()
        }
