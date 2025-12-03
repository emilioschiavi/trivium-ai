#!/usr/bin/env python
"""
Milestone 5.1 Testing Script
Tests all application functionality systematically
"""

import sys
import time
import json
from urllib import request
from urllib.error import URLError, HTTPError


def test_server_running():
    """Test 1: Verify server is running"""
    print("\n" + "="*60)
    print("TEST 1: Server Running Check")
    print("="*60)
    
    try:
        response = request.urlopen('http://127.0.0.1:8000/', timeout=5)
        status = response.getcode()
        print("✅ Server is running")
        print("   Status Code: {}".format(status))
        return True
    except (URLError, HTTPError) as e:
        print("❌ Server is not accessible: {}".format(e))
        return False


def test_weather_data():
    """Test 2: Verify weather data displays correctly"""
    print("\n" + "="*60)
    print("TEST 2: Weather Data Display")
    print("="*60)
    
    try:
        response = request.urlopen('http://127.0.0.1:8000/', timeout=5)
        html_content = response.read().decode('utf-8')
        
        # Check for weather data elements
        checks = {
            'Temperature display': '°C' in html_content,
            'Location name': 'Reinach' in html_content,
            'Weather description': 'weather-icon' in html_content or 'description' in html_content,
            'Humidity': 'Humidity' in html_content,
            'Wind speed': 'Wind' in html_content,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print("   {}: {}".format(status, check_name))
            if not result:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print("❌ Failed to fetch weather data: {}".format(e))
        return False


def test_sport_recommendations():
    """Test 3: Verify sport recommendations are displayed"""
    print("\n" + "="*60)
    print("TEST 3: Sport Recommendations")
    print("="*60)
    
    try:
        response = request.urlopen('http://127.0.0.1:8000/', timeout=5)
        html_content = response.read().decode('utf-8')
        
        checks = {
            'Cycling section': 'Cycling' in html_content,
            'Running section': 'Running' in html_content,
            'Recommendations container': 'recommendations' in html_content.lower(),
            'Sport cards': 'sport-card' in html_content,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print("   {}: {}".format(status, check_name))
            if not result:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print("❌ Failed to check sport recommendations: {}".format(e))
        return False


def test_charts_setup():
    """Test 4: Verify charts are set up correctly"""
    print("\n" + "="*60)
    print("TEST 4: Charts Setup")
    print("="*60)
    
    try:
        response = request.urlopen('http://127.0.0.1:8000/', timeout=5)
        html_content = response.read().decode('utf-8')
        
        checks = {
            'Chart.js library': 'chart.js' in html_content.lower(),
            'Temperature chart canvas': 'temperatureChart' in html_content,
            'Precipitation chart canvas': 'precipitationChart' in html_content,
            'Wind chart canvas': 'windChart' in html_content,
            'Charts JavaScript': 'charts.js' in html_content,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print("   {}: {}".format(status, check_name))
            if not result:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print("❌ Failed to check charts setup: {}".format(e))
        return False


def test_preferences_form():
    """Test 5: Verify preferences form is present"""
    print("\n" + "="*60)
    print("TEST 5: Preferences Form")
    print("="*60)
    
    try:
        response = request.urlopen('http://127.0.0.1:8000/', timeout=5)
        html_content = response.read().decode('utf-8')
        
        checks = {
            'Preferences form': 'preferencesForm' in html_content,
            'Cycling temperature inputs': 'cyclingTempMin' in html_content and 'cyclingTempMax' in html_content,
            'Running temperature inputs': 'runningTempMin' in html_content and 'runningTempMax' in html_content,
            'Wind speed input': 'windMax' in html_content,
            'Rain threshold inputs': 'cyclingRainMax' in html_content and 'runningRainMax' in html_content,
            'Save button': 'type="submit"' in html_content,
            'Reset button': 'resetBtn' in html_content or 'type="reset"' in html_content,
            'Preferences JavaScript': 'preferences.js' in html_content,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print("   {}: {}".format(status, check_name))
            if not result:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print("❌ Failed to check preferences form: {}".format(e))
        return False


def test_static_files():
    """Test 6: Verify static files are accessible"""
    print("\n" + "="*60)
    print("TEST 6: Static Files Accessibility")
    print("="*60)
    
    static_files = {
        'CSS': 'http://127.0.0.1:8000/static/css/styles.css',
        'Main JS': 'http://127.0.0.1:8000/static/js/main.js',
        'Preferences JS': 'http://127.0.0.1:8000/static/js/preferences.js',
        'Charts JS': 'http://127.0.0.1:8000/static/js/charts.js',
    }
    
    all_passed = True
    for name, url in static_files.items():
        try:
            response = request.urlopen(url, timeout=5)
            status = response.getcode()
            size = len(response.read())
            print("   ✅ {}: {} ({} bytes)".format(name, status, size))
        except Exception as e:
            print("   ❌ {}: Failed - {}".format(name, e))
            all_passed = False
    
    return all_passed


def test_responsive_design():
    """Test 7: Check for responsive design elements"""
    print("\n" + "="*60)
    print("TEST 7: Responsive Design Elements")
    print("="*60)
    
    try:
        response = request.urlopen('http://127.0.0.1:8000/static/css/styles.css', timeout=5)
        css_content = response.read().decode('utf-8')
        
        checks = {
            'Viewport meta tag needed': True,  # Will check in HTML
            'Media queries present': '@media' in css_content,
            'Mobile breakpoint (768px)': '768px' in css_content,
            'Desktop breakpoint (1024px)': '1024px' in css_content,
            'Flexible grid/flexbox': 'flex' in css_content or 'grid' in css_content,
        }
        
        # Check HTML for viewport
        html_response = request.urlopen('http://127.0.0.1:8000/', timeout=5)
        html_content = html_response.read().decode('utf-8')
        checks['Viewport meta tag'] = 'viewport' in html_content
        
        all_passed = True
        for check_name, result in checks.items():
            if check_name == 'Viewport meta tag needed':
                continue
            status = "✅" if result else "❌"
            print("   {}: {}".format(status, check_name))
            if not result:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print("❌ Failed to check responsive design: {}".format(e))
        return False


def test_error_handling():
    """Test 8: Check for error handling elements"""
    print("\n" + "="*60)
    print("TEST 8: Error Handling Elements")
    print("="*60)
    
    try:
        response = request.urlopen('http://127.0.0.1:8000/', timeout=5)
        html_content = response.read().decode('utf-8')
        
        # Check JavaScript files for error handling
        js_urls = [
            'http://127.0.0.1:8000/static/js/main.js',
            'http://127.0.0.1:8000/static/js/preferences.js',
        ]
        
        error_handling_found = False
        for url in js_urls:
            js_response = request.urlopen(url, timeout=5)
            js_content = js_response.read().decode('utf-8')
            if 'try' in js_content or 'catch' in js_content or 'error' in js_content.lower():
                error_handling_found = True
                break
        
        checks = {
            'JavaScript error handling': error_handling_found,
            'Notification container': 'id="notification"' in html_content,
            'Notification CSS class': 'class="notification"' in html_content,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "✅" if result else "❌"
            print("   {}: {}".format(status, check_name))
            if not result:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print("❌ Failed to check error handling: {}".format(e))
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "="*80)
    print(" MILESTONE 5.1 COMPREHENSIVE TESTING")
    print("="*80)
    print("\nTesting Swiss Weather Sport Planner Application")
    print("Target: http://127.0.0.1:8000/")
    print("Date: December 3, 2025")
    
    tests = [
        ("Server Running", test_server_running),
        ("Weather Data Display", test_weather_data),
        ("Sport Recommendations", test_sport_recommendations),
        ("Charts Setup", test_charts_setup),
        ("Preferences Form", test_preferences_form),
        ("Static Files", test_static_files),
        ("Responsive Design", test_responsive_design),
        ("Error Handling", test_error_handling),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print("\n❌ Test '{}' crashed: {}".format(test_name, e))
            results.append((test_name, False))
        time.sleep(0.5)  # Small delay between tests
    
    # Summary
    print("\n" + "="*80)
    print(" TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print("   {}: {}".format(status, test_name))
    
    print("\n" + "-"*80)
    print("   Total: {}/{} tests passed ({:.1f}%)".format(
        passed, total, (passed / total * 100) if total > 0 else 0
    ))
    print("="*80)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Application is ready for Milestone 5.2")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review issues above.")
        return 1


if __name__ == '__main__':
    try:
        sys.exit(run_all_tests())
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
        sys.exit(1)
