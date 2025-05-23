# Exercise 15: AI Agent for Weather Data

import requests
import os
from datetime import datetime
from typing import Dict, Any, Optional, Union
import json

class WeatherAgent:
    """
    An AI agent that fetches real-time weather data from OpenWeatherMap API
    and responds with the current temperature and weather conditions.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the weather agent with an API key.
        
        Args:
            api_key: OpenWeatherMap API key. If None, it will try to get it from
                    the OPENWEATHER_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.units = "metric"  # Use metric units (Celsius)
        
        if not self.api_key:
            print("Warning: No API key provided. You'll need to set one before making requests.")
    
    def set_api_key(self, api_key: str) -> None:
        """Set the OpenWeatherMap API key."""
        self.api_key = api_key
    
    def set_units(self, units: str) -> None:
        """
        Set the units for temperature.
        
        Args:
            units: One of 'metric' (Celsius), 'imperial' (Fahrenheit), or 'standard' (Kelvin)
        """
        if units not in ["metric", "imperial", "standard"]:
            raise ValueError("Units must be one of: metric, imperial, standard")
        self.units = units
    
    def get_weather_by_city(self, city: str) -> Dict[str, Any]:
        """
        Get current weather data for a city.
        
        Args:
            city: City name, optionally with country code (e.g., 'London,UK')
            
        Returns:
            Dictionary with weather data or error information
        """
        if not self.api_key:
            return {"error": "API key not set. Use set_api_key() method or set OPENWEATHER_API_KEY environment variable."}
        
        params = {
            "q": city,
            "appid": self.api_key,
            "units": self.units
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return {"error": f"City '{city}' not found"}
            elif response.status_code == 401:
                return {"error": "Invalid API key"}
            else:
                return {"error": f"HTTP Error: {str(e)}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Failed to parse API response"}
    
    def get_weather_by_coordinates(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get current weather data for a location by coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary with weather data or error information
        """
        if not self.api_key:
            return {"error": "API key not set. Use set_api_key() method or set OPENWEATHER_API_KEY environment variable."}
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": self.units
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                return {"error": "Invalid API key"}
            else:
                return {"error": f"HTTP Error: {str(e)}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Failed to parse API response"}
    
    def format_weather_response(self, weather_data: Dict[str, Any]) -> str:
        """
        Format the weather data into a human-readable response.
        
        Args:
            weather_data: Dictionary with weather data from the API
            
        Returns:
            Formatted string with weather information
        """
        if "error" in weather_data:
            return f"Error: {weather_data['error']}"
        
        try:
            city = weather_data["name"]
            country = weather_data["sys"]["country"]
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            description = weather_data["weather"][0]["description"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]
            
            # Get unit symbol
            temp_unit = "°C" if self.units == "metric" else "°F" if self.units == "imperial" else "K"
            speed_unit = "m/s" if self.units == "metric" else "mph"
            
            # Format timestamp
            timestamp = weather_data["dt"]
            datetime_obj = datetime.fromtimestamp(timestamp)
            time_str = datetime_obj.strftime("%H:%M:%S")
            date_str = datetime_obj.strftime("%Y-%m-%d")
            
            return (
                f"Weather in {city}, {country} at {time_str} on {date_str}:\n"
                f"Temperature: {temp}{temp_unit} (Feels like: {feels_like}{temp_unit})\n"
                f"Conditions: {description.capitalize()}\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} {speed_unit}"
            )
        except (KeyError, IndexError) as e:
            return f"Error parsing weather data: {str(e)}"
    
    def get_temperature(self, location: str) -> str:
        """
        Get only the current temperature for a location.
        
        Args:
            location: City name or "lat,lon" coordinates
            
        Returns:
            String with temperature information or error message
        """
        # Check if location is coordinates (format: "lat,lon")
        if "," in location and all(part.replace(".", "", 1).replace("-", "", 1).isdigit() 
                                  for part in location.split(",")):
            lat, lon = map(float, location.split(","))
            weather_data = self.get_weather_by_coordinates(lat, lon)
        else:
            weather_data = self.get_weather_by_city(location)
        
        if "error" in weather_data:
            return f"Error: {weather_data['error']}"
        
        try:
            city = weather_data["name"]
            country = weather_data["sys"]["country"]
            temp = weather_data["main"]["temp"]
            
            # Get unit symbol
            temp_unit = "°C" if self.units == "metric" else "°F" if self.units == "imperial" else "K"
            
            return f"The current temperature in {city}, {country} is {temp}{temp_unit}."
        except (KeyError, IndexError) as e:
            return f"Error parsing weather data: {str(e)}"
    
    def respond(self, query: str) -> str:
        """
        Respond to a user query about weather.
        
        Args:
            query: User's weather query
            
        Returns:
            Response with weather information
        """
        # Extract location from query
        query = query.lower()
        
        # Handle help requests
        if "help" in query or "how to use" in query:
            return (
                "I can provide weather information for any location. Try asking:\n"
                "- What's the weather in London?\n"
                "- Temperature in New York\n"
                "- Weather conditions in Tokyo\n"
                "- Current weather at coordinates 40.7,-74.0"
            )
        
        # Handle API key instructions
        if "api key" in query or "apikey" in query:
            return (
                "To use this weather agent, you need an OpenWeatherMap API key. You can:\n"
                "1. Sign up for a free API key at https://openweathermap.org/\n"
                "2. Set the API key using agent.set_api_key('your_api_key')\n"
                "3. Or set the OPENWEATHER_API_KEY environment variable"
            )
        
        # Check if API key is set
        if not self.api_key:
            return "I need an API key to fetch weather data. Use set_api_key() method or set the OPENWEATHER_API_KEY environment variable."
        
        # Extract location from query
        if "coordinates" in query or "coords" in query:
            # Try to extract coordinates (format like "40.7,-74.0")
            import re
            coords_match = re.search(r'(-?\d+\.?\d*),\s*(-?\d+\.?\d*)', query)
            if coords_match:
                lat, lon = map(float, coords_match.groups())
                weather_data = self.get_weather_by_coordinates(lat, lon)
                return self.format_weather_response(weather_data)
            else:
                return "I couldn't find valid coordinates in your query. Please provide them in the format 'latitude,longitude'."
        
        # Common location extraction patterns
        location_patterns = [
            r'weather (?:in|at|for) ([\w\s,]+)(?:\?)?$',
            r'temperature (?:in|at|for) ([\w\s,]+)(?:\?)?$',
            r'weather (?:of|for) ([\w\s,]+)(?:\?)?$',
            r'what\'s the weather (?:in|at) ([\w\s,]+)(?:\?)?$',
            r'how\'s the weather (?:in|at) ([\w\s,]+)(?:\?)?$',
            r'^([\w\s,]+) weather$',
        ]
        
        for pattern in location_patterns:
            import re
            match = re.search(pattern, query)
            if match:
                location = match.group(1).strip()
                
                # Determine the type of response based on the query
                if "temperature" in query or "temp" in query:
                    return self.get_temperature(location)
                else:
                    weather_data = self.get_weather_by_city(location)
                    return self.format_weather_response(weather_data)
        
        # If no pattern matched, try to extract the location as the last word
        words = query.split()
        if len(words) > 0:
            potential_location = words[-1].strip("?.,!")
            if len(potential_location) > 2:  # Avoid very short potential locations
                weather_data = self.get_weather_by_city(potential_location)
                if "error" not in weather_data or "not found" not in weather_data.get("error", ""):
                    return self.format_weather_response(weather_data)
        
        return "I'm not sure what location you're asking about. Try a query like 'What's the weather in London?' or 'Temperature in Tokyo'."


if __name__ == "__main__":
    # Example usage
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    agent = WeatherAgent(api_key)
    
    if not api_key:
        print("No API key found. Please set your OpenWeatherMap API key:")
        print("1. Sign up at https://openweathermap.org/ to get a free API key")
        print("2. Set the OPENWEATHER_API_KEY environment variable or provide it as an argument")
        print("\nSimulating responses without making actual API calls...\n")
        
        # Simulate responses for demonstration
        print("Query: What's the weather in London?")
        print("Response: The current temperature in London, GB is 15.2°C.")
        print("\nQuery: Temperature in New York")
        print("Response: The current temperature in New York, US is 22.8°C.")
        print("\nQuery: Weather conditions in Tokyo")
        print("Weather in Tokyo, JP at 15:30:45 on 2023-05-20:")
        print("Temperature: 24.5°C (Feels like: 25.1°C)")
        print("Conditions: Partly cloudy")
        print("Humidity: 65%")
        print("Wind Speed: 3.2 m/s")
    else:
        # Use real API with the provided key
        print("API key found. Testing with real data...")
        
        # Test with a few example queries
        test_queries = [
            "What's the weather in London?",
            "Temperature in New York",
            "How's the weather in Tokyo?",
            "Paris weather"
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            response = agent.respond(query)
            print(f"Response: {response}")