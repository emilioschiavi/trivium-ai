from django.shortcuts import render
from django.http import JsonResponse
from .services.weather_service import WeatherService
from .services.sport_service import SportRecommendationService
import logging
import json

logger = logging.getLogger(__name__)


def index(request):
    """
    Main view for the weather sport planner application.
    
    Fetches current weather data and 24-hour forecast for Reinach BL,
    generates sport recommendations based on weather conditions,
    and renders the main template with all necessary data.
    
    Args:
        request: Django HTTP request object
        
    Returns:
        HttpResponse: Rendered template with weather and sport data
    """
    context = {
        'error': None,
        'current_weather': None,
        'forecast_24h': None,
        'cycling_recommendation': None,
        'running_recommendation': None,
    }
    
    try:
        # Initialize weather service
        weather_service = WeatherService()
        
        # Fetch current weather
        current_weather = weather_service.get_current_weather()
        context['current_weather'] = current_weather
        
        # Fetch 24-hour forecast
        forecast_24h = weather_service.get_forecast_24h()
        context['forecast_24h'] = forecast_24h
        
        # Convert forecast data to JSON-serializable format
        if forecast_24h:
            forecast_json_data = []
            for item in forecast_24h:
                forecast_json_data.append({
                    'timestamp': item['timestamp'].isoformat() if hasattr(item['timestamp'], 'isoformat') else str(item['timestamp']),
                    'temperature': item['temperature'],
                    'wind_speed': item['wind_speed'],
                    'precipitation': item['precipitation'],
                    'humidity': item['humidity'],
                    'description': item['description']
                })
            context['forecast_json'] = json.dumps(forecast_json_data)
        else:
            context['forecast_json'] = '[]'
        
        # Initialize sport service with default thresholds
        sport_service = SportRecommendationService()
        
        # Get cycling recommendation
        cycling_recommended, cycling_reasons = sport_service.evaluate_sport(
            sport='cycling',
            weather_data=current_weather
        )
        context['cycling_recommendation'] = {
            'recommended': cycling_recommended,
            'reason': ' '.join(cycling_reasons)
        }
        
        # Get running recommendation
        running_recommended, running_reasons = sport_service.evaluate_sport(
            sport='running',
            weather_data=current_weather
        )
        context['running_recommendation'] = {
            'recommended': running_recommended,
            'reason': ' '.join(running_reasons)
        }
        
    except Exception as e:
        logger.error("Error fetching weather data or generating recommendations: {}".format(str(e)))
        context['error'] = "Unable to fetch weather data. Please try again later."
    
    return render(request, 'weather_app/index.html', context)
