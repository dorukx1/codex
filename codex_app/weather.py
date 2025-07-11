import os
import requests
from typing import Any, Dict

def fetch_weather(city: str, api_key: str = None) -> Dict[str, Any]:
    """Fetch current weather and 5 day forecast for a city using OpenWeatherMap API."""
    api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OpenWeatherMap API key not provided. Set OPENWEATHER_API_KEY env variable.")
    base_url = "https://api.openweathermap.org/data/2.5"
    current_url = f"{base_url}/weather?q={city}&appid={api_key}&units=metric"
    forecast_url = f"{base_url}/forecast?q={city}&appid={api_key}&units=metric"
    current_resp = requests.get(current_url)
    forecast_resp = requests.get(forecast_url)
    current_resp.raise_for_status()
    forecast_resp.raise_for_status()
    return {
        "current": current_resp.json(),
        "forecast": forecast_resp.json(),
    }
