"""
Sport Recommendation Service
Evaluates weather conditions to recommend suitable outdoor sports
"""

from typing import Dict, List, Optional, Tuple


class SportRecommendationService:
    """Service for generating sport recommendations based on weather conditions"""
    
    # Default thresholds for each sport
    DEFAULT_THRESHOLDS = {
        'cycling': {
            'temp_min': 15,  # °C
            'temp_max': 25,  # °C
            'wind_max': 30,  # km/h
            'rain_max': 0,   # mm/h
        },
        'running': {
            'temp_min': 10,  # °C
            'temp_max': 20,  # °C
            'wind_max': 30,  # km/h
            'rain_max': 3,   # mm/h
        }
    }
    
    def __init__(self, custom_thresholds: Optional[Dict] = None):
        """
        Initialize the sport recommendation service
        
        Args:
            custom_thresholds: Optional custom thresholds to override defaults
        """
        self.thresholds = self.DEFAULT_THRESHOLDS.copy()
        if custom_thresholds:
            for sport, values in custom_thresholds.items():
                if sport in self.thresholds:
                    self.thresholds[sport].update(values)
                else:
                    self.thresholds[sport] = values
    
    def evaluate_sport(self, sport: str, weather_data: Dict) -> Tuple[bool, List[str]]:
        """
        Evaluate if conditions are suitable for a specific sport
        
        Args:
            sport: Name of the sport ('cycling' or 'running')
            weather_data: Dictionary containing temperature, wind_speed, and rain
            
        Returns:
            Tuple of (is_recommended: bool, reasons: List[str])
        """
        if sport not in self.thresholds:
            return False, [f"Unknown sport: {sport}"]
        
        thresholds = self.thresholds[sport]
        temperature = weather_data.get('temperature', 0)
        wind_speed = weather_data.get('wind_speed', 0)
        rain = weather_data.get('rain', 0)
        
        reasons = []
        is_suitable = True
        
        # Check temperature
        if temperature < thresholds['temp_min']:
            is_suitable = False
            reasons.append(
                f"Too cold: {temperature:.1f}°C (minimum: {thresholds['temp_min']}°C)"
            )
        elif temperature > thresholds['temp_max']:
            is_suitable = False
            reasons.append(
                f"Too hot: {temperature:.1f}°C (maximum: {thresholds['temp_max']}°C)"
            )
        else:
            reasons.append(
                f"Temperature perfect: {temperature:.1f}°C"
            )
        
        # Check wind speed
        if wind_speed > thresholds['wind_max']:
            is_suitable = False
            reasons.append(
                f"Too windy: {wind_speed:.1f} km/h (maximum: {thresholds['wind_max']} km/h)"
            )
        else:
            reasons.append(
                f"Wind acceptable: {wind_speed:.1f} km/h"
            )
        
        # Check rain
        if rain > thresholds['rain_max']:
            is_suitable = False
            if thresholds['rain_max'] == 0:
                reasons.append(
                    f"Raining: {rain:.1f} mm/h (requires no rain)"
                )
            else:
                reasons.append(
                    f"Too much rain: {rain:.1f} mm/h (maximum: {thresholds['rain_max']} mm/h)"
                )
        else:
            if rain > 0:
                reasons.append(
                    f"Light rain acceptable: {rain:.1f} mm/h"
                )
            else:
                reasons.append("No rain - perfect conditions")
        
        return is_suitable, reasons
    
    def get_recommendations(self, weather_data: Dict) -> Dict:
        """
        Generate sport recommendations based on current weather
        
        Args:
            weather_data: Dictionary containing temperature, wind_speed, and rain
            
        Returns:
            Dictionary with recommendations for each sport
        """
        recommendations = {}
        
        for sport in self.thresholds.keys():
            is_recommended, reasons = self.evaluate_sport(sport, weather_data)
            
            recommendations[sport] = {
                'recommended': is_recommended,
                'reasons': reasons,
                'summary': self._generate_summary(sport, is_recommended, reasons)
            }
        
        return recommendations
    
    def get_recommendations_for_forecast(self, forecast_data: List[Dict]) -> List[Dict]:
        """
        Generate sport recommendations for forecast periods
        
        Args:
            forecast_data: List of weather dictionaries for each forecast period
            
        Returns:
            List of recommendation dictionaries for each period
        """
        forecast_recommendations = []
        
        for period in forecast_data:
            weather = {
                'temperature': period.get('temperature', 0),
                'wind_speed': period.get('wind_speed', 0),
                'rain': period.get('rain', 0)
            }
            
            recommendations = self.get_recommendations(weather)
            
            forecast_recommendations.append({
                'timestamp': period.get('timestamp'),
                'time': period.get('time'),
                'weather': weather,
                'recommendations': recommendations
            })
        
        return forecast_recommendations
    
    def _generate_summary(self, sport: str, is_recommended: bool, reasons: List[str]) -> str:
        """
        Generate a human-readable summary of the recommendation
        
        Args:
            sport: Name of the sport
            is_recommended: Whether the sport is recommended
            reasons: List of reason strings
            
        Returns:
            Summary text
        """
        sport_name = sport.capitalize()
        
        if is_recommended:
            return f"✅ Great conditions for {sport_name}! {' '.join(reasons)}"
        else:
            negative_reasons = [r for r in reasons if 'Too' in r or 'Raining' in r or 'rain' in r.lower()]
            if negative_reasons:
                return f"❌ Not ideal for {sport_name}. {' '.join(negative_reasons)}"
            else:
                return f"❌ Conditions not suitable for {sport_name}."
    
    def update_thresholds(self, sport: str, new_thresholds: Dict):
        """
        Update thresholds for a specific sport
        
        Args:
            sport: Name of the sport
            new_thresholds: Dictionary with new threshold values
        """
        if sport not in self.thresholds:
            self.thresholds[sport] = {}
        
        self.thresholds[sport].update(new_thresholds)
    
    def get_all_thresholds(self) -> Dict:
        """
        Get all current thresholds
        
        Returns:
            Dictionary of all sport thresholds
        """
        return self.thresholds.copy()
    
    def get_best_times(self, forecast_recommendations: List[Dict], sport: str) -> List[Dict]:
        """
        Find the best times for a specific sport from forecast
        
        Args:
            forecast_recommendations: List of forecast recommendations
            sport: Name of the sport to check
            
        Returns:
            List of suitable time periods for the sport
        """
        best_times = []
        
        for period in forecast_recommendations:
            if sport in period['recommendations']:
                if period['recommendations'][sport]['recommended']:
                    best_times.append({
                        'time': period['time'],
                        'timestamp': period['timestamp'],
                        'weather': period['weather'],
                        'reasons': period['recommendations'][sport]['reasons']
                    })
        
        return best_times
