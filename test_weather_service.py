"""
Test script for Weather Service
Run this to verify OpenWeatherMap API integration
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_project.settings')
django.setup()

from weather_app.services import WeatherService


def test_weather_service():
    """Test the Weather Service API integration"""
    
    print("=" * 60)
    print("Testing Weather Service API Integration")
    print("=" * 60)
    
    service = WeatherService()
    
    # Test current weather
    print("\n1. Testing Current Weather for Reinach BL...")
    print("-" * 60)
    
    current = service.get_current_weather()
    
    if current:
        print("✅ Current Weather Retrieved Successfully!")
        print(f"   Location: {current['location']}")
        print(f"   Temperature: {current['temperature']:.1f}°C")
        print(f"   Feels Like: {current['feels_like']:.1f}°C")
        print(f"   Wind Speed: {current['wind_speed']:.1f} km/h")
        print(f"   Precipitation: {current['precipitation']} mm/h")
        print(f"   Humidity: {current['humidity']}%")
        print(f"   Description: {current['description']}")
        print(f"   Timestamp: {current['timestamp']}")
    else:
        print("❌ Failed to retrieve current weather")
        return False
    
    # Test 24-hour forecast
    print("\n2. Testing 24-Hour Forecast...")
    print("-" * 60)
    
    forecast = service.get_forecast_24h()
    
    if forecast:
        print(f"✅ 24-Hour Forecast Retrieved Successfully!")
        print(f"   Retrieved {len(forecast)} forecast periods")
        print("\n   Forecast Summary:")
        
        for i, period in enumerate(forecast[:3], 1):  # Show first 3 periods
            print(f"\n   Period {i}:")
            print(f"      Time: {period['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            print(f"      Temperature: {period['temperature']:.1f}°C")
            print(f"      Wind Speed: {period['wind_speed']:.1f} km/h")
            print(f"      Precipitation: {period['precipitation']} mm/3h")
            print(f"      Description: {period['description']}")
        
        if len(forecast) > 3:
            print(f"\n   ... and {len(forecast) - 3} more periods")
    else:
        print("❌ Failed to retrieve forecast")
        return False
    
    # Test caching
    print("\n3. Testing Cache (should be instant)...")
    print("-" * 60)
    
    import time
    start = time.time()
    cached_current = service.get_current_weather()
    end = time.time()
    
    if cached_current and (end - start) < 0.1:
        print(f"✅ Cache Working! Response time: {(end - start) * 1000:.2f}ms")
    else:
        print("⚠️  Cache might not be working as expected")
    
    print("\n" + "=" * 60)
    print("Weather Service Test Complete!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = test_weather_service()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
