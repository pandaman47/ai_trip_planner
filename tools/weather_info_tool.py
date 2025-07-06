import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from langchain.tools import tool
from utils.weather_info import WeatherForecastTool
load_dotenv()

class WeatherInfoTool:
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.getenv("WEATHER_API_KEY")
        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Set up the weather and weather forecast tools."""
        @tool
        def get_current_weather(city: str) -> str:
            """Get current weather for a given city."""
            weather_data = self.weather_service.get_current_weather(city)
            if weather_data:
                temp = weather_data.get('main', {}).get("temp","N/A")
                description = weather_data.get('weather', [{}])[0].get("description", "N/A")
                return f"Current temperature in {city} is {temp}°C with {description}."
            return f"Could not retrieve weather data for {city}."
    
        @tool
        def get_weather_forecast(city: str) -> str:
            """Get the weather forecast for a given city."""
            forecast_data = self.weather_service.get_forecast_weather(city)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(" ")[0]
                    temp = item['main'].get('temp', 'N/A')
                    description = item['weather'][0].get('description', 'N/A')
                    forecast_summary.append(f"Date: {date}, Temp: {temp}°C, Description: {description}")
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Could not retrieve weather forecast data for {city}."
        
        return [get_current_weather, get_weather_forecast]
        