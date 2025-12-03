"""
Tests for Django views
"""

from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock


class IndexViewTests(TestCase):
    """Tests for the main index view"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse('index')
    
    @patch('weather_app.views.WeatherService')
    @patch('weather_app.views.SportRecommendationService')
    def test_index_view_success(self, mock_sport_service, mock_weather_service):
        """Test successful rendering of index view with weather data"""
        # Mock weather service
        mock_weather = MagicMock()
        mock_weather.get_current_weather.return_value = {
            'temperature': 18.5,
            'wind_speed': 15.0,
            'humidity': 65,
            'precipitation': 0.0,
        }
        mock_weather.get_forecast_24h.return_value = []
        mock_weather_service.return_value = mock_weather
        
        # Mock sport service
        mock_sport = MagicMock()
        mock_sport.evaluate_sport.side_effect = [
            (True, ['Good conditions for cycling']),
            (True, ['Good conditions for running'])
        ]
        mock_sport_service.return_value = mock_sport
        
        # Make request
        response = self.client.get(self.url)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather_app/index.html')
        self.assertIn('current_weather', response.context)
        self.assertIn('cycling_recommendation', response.context)
        self.assertIn('running_recommendation', response.context)
    
    @patch('weather_app.views.WeatherService')
    def test_index_view_error_handling(self, mock_weather_service):
        """Test error handling when weather service fails"""
        # Mock weather service to raise exception
        mock_weather = MagicMock()
        mock_weather.get_current_weather.side_effect = Exception('API Error')
        mock_weather_service.return_value = mock_weather
        
        # Make request
        response = self.client.get(self.url)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.context)
        self.assertIsNotNone(response.context['error'])
    
    def test_index_view_accessible(self):
        """Test that index view is accessible at root URL"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
