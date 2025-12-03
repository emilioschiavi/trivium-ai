"""
Test script for Sport Recommendation Service
"""

import sys
import os

# Add the parent directory to the path to import weather_app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from weather_app.services.sport_service import SportRecommendationService


def test_perfect_cycling_conditions():
    """Test cycling recommendations with perfect conditions"""
    print("\n=== Test 1: Perfect Cycling Conditions ===")
    service = SportRecommendationService()
    
    weather = {
        'temperature': 20,  # Perfect for cycling
        'wind_speed': 15,   # Light wind
        'rain': 0           # No rain
    }
    
    recommendations = service.get_recommendations(weather)
    
    print(f"Weather: {weather}")
    print(f"\nCycling: {recommendations['cycling']['recommended']}")
    print(f"Summary: {recommendations['cycling']['summary']}")
    print(f"Reasons: {recommendations['cycling']['reasons']}")
    
    assert recommendations['cycling']['recommended'] == True
    print("✅ Test passed!")


def test_too_cold_for_cycling():
    """Test cycling recommendations when too cold"""
    print("\n=== Test 2: Too Cold for Cycling ===")
    service = SportRecommendationService()
    
    weather = {
        'temperature': 5,   # Too cold
        'wind_speed': 15,
        'rain': 0
    }
    
    recommendations = service.get_recommendations(weather)
    
    print(f"Weather: {weather}")
    print(f"\nCycling: {recommendations['cycling']['recommended']}")
    print(f"Summary: {recommendations['cycling']['summary']}")
    
    assert recommendations['cycling']['recommended'] == False
    print("✅ Test passed!")


def test_too_windy():
    """Test when conditions are too windy"""
    print("\n=== Test 3: Too Windy ===")
    service = SportRecommendationService()
    
    weather = {
        'temperature': 18,
        'wind_speed': 35,   # Too windy
        'rain': 0
    }
    
    recommendations = service.get_recommendations(weather)
    
    print(f"Weather: {weather}")
    print(f"\nCycling: {recommendations['cycling']['recommended']}")
    print(f"Running: {recommendations['running']['recommended']}")
    
    assert recommendations['cycling']['recommended'] == False
    assert recommendations['running']['recommended'] == False
    print("✅ Test passed!")


def test_light_rain_running():
    """Test running with light rain (acceptable)"""
    print("\n=== Test 4: Light Rain for Running ===")
    service = SportRecommendationService()
    
    weather = {
        'temperature': 15,
        'wind_speed': 10,
        'rain': 2           # Light rain, acceptable for running
    }
    
    recommendations = service.get_recommendations(weather)
    
    print(f"Weather: {weather}")
    print(f"\nRunning: {recommendations['running']['recommended']}")
    print(f"Summary: {recommendations['running']['summary']}")
    print(f"\nCycling: {recommendations['cycling']['recommended']}")
    
    assert recommendations['running']['recommended'] == True
    assert recommendations['cycling']['recommended'] == False  # Cycling requires no rain
    print("✅ Test passed!")


def test_heavy_rain():
    """Test when it's raining too much"""
    print("\n=== Test 5: Heavy Rain ===")
    service = SportRecommendationService()
    
    weather = {
        'temperature': 18,
        'wind_speed': 10,
        'rain': 5           # Too much rain
    }
    
    recommendations = service.get_recommendations(weather)
    
    print(f"Weather: {weather}")
    print(f"\nRunning: {recommendations['running']['recommended']}")
    print(f"Cycling: {recommendations['cycling']['recommended']}")
    
    assert recommendations['running']['recommended'] == False
    assert recommendations['cycling']['recommended'] == False
    print("✅ Test passed!")


def test_custom_thresholds():
    """Test with custom thresholds"""
    print("\n=== Test 6: Custom Thresholds ===")
    
    custom_thresholds = {
        'cycling': {
            'temp_min': 10,  # More tolerant to cold
            'temp_max': 30,  # More tolerant to heat
        }
    }
    
    service = SportRecommendationService(custom_thresholds=custom_thresholds)
    
    weather = {
        'temperature': 12,  # Would be too cold with defaults
        'wind_speed': 15,
        'rain': 0
    }
    
    recommendations = service.get_recommendations(weather)
    
    print(f"Weather: {weather}")
    print(f"Custom thresholds: {custom_thresholds}")
    print(f"\nCycling: {recommendations['cycling']['recommended']}")
    print(f"Summary: {recommendations['cycling']['summary']}")
    
    assert recommendations['cycling']['recommended'] == True
    print("✅ Test passed!")


def test_forecast_recommendations():
    """Test forecast recommendations"""
    print("\n=== Test 7: Forecast Recommendations ===")
    service = SportRecommendationService()
    
    forecast_data = [
        {'timestamp': '2024-01-01 09:00', 'time': '09:00', 'temperature': 12, 'wind_speed': 20, 'rain': 0},
        {'timestamp': '2024-01-01 12:00', 'time': '12:00', 'temperature': 18, 'wind_speed': 15, 'rain': 0},
        {'timestamp': '2024-01-01 15:00', 'time': '15:00', 'temperature': 22, 'wind_speed': 10, 'rain': 0},
        {'timestamp': '2024-01-01 18:00', 'time': '18:00', 'temperature': 16, 'wind_speed': 25, 'rain': 1},
    ]
    
    forecast_recs = service.get_recommendations_for_forecast(forecast_data)
    
    print(f"\nForecast periods analyzed: {len(forecast_recs)}")
    for period in forecast_recs:
        print(f"\n{period['time']}: Temp={period['weather']['temperature']}°C")
        print(f"  Cycling: {period['recommendations']['cycling']['recommended']}")
        print(f"  Running: {period['recommendations']['running']['recommended']}")
    
    # Find best times for cycling
    best_cycling = service.get_best_times(forecast_recs, 'cycling')
    print(f"\nBest times for cycling: {len(best_cycling)} periods")
    for time in best_cycling:
        print(f"  - {time['time']}")
    
    print("✅ Test passed!")


def test_edge_cases():
    """Test edge cases"""
    print("\n=== Test 8: Edge Cases ===")
    service = SportRecommendationService()
    
    # Extreme cold
    weather_extreme_cold = {'temperature': -10, 'wind_speed': 5, 'rain': 0}
    recs = service.get_recommendations(weather_extreme_cold)
    assert recs['cycling']['recommended'] == False
    assert recs['running']['recommended'] == False
    print("✅ Extreme cold handled correctly")
    
    # Extreme heat
    weather_extreme_heat = {'temperature': 35, 'wind_speed': 5, 'rain': 0}
    recs = service.get_recommendations(weather_extreme_heat)
    assert recs['cycling']['recommended'] == False
    assert recs['running']['recommended'] == False
    print("✅ Extreme heat handled correctly")
    
    # No sports recommended
    weather_bad = {'temperature': 5, 'wind_speed': 40, 'rain': 10}
    recs = service.get_recommendations(weather_bad)
    assert recs['cycling']['recommended'] == False
    assert recs['running']['recommended'] == False
    print("✅ Multiple bad conditions handled correctly")
    
    print("✅ All edge cases passed!")


def main():
    """Run all tests"""
    print("=" * 60)
    print("SPORT RECOMMENDATION SERVICE TESTS")
    print("=" * 60)
    
    try:
        test_perfect_cycling_conditions()
        test_too_cold_for_cycling()
        test_too_windy()
        test_light_rain_running()
        test_heavy_rain()
        test_custom_thresholds()
        test_forecast_recommendations()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
