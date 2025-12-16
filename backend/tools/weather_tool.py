import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city: str) -> dict:
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        return {"error": "Weather API key not configured."}

    base_url = "https://api.openweathermap.org/data/2.5/weather"

    queries = [city, f"{city},IN"]

    for q in queries:
        try:
            params = {
                "q": q,
                "appid": api_key,
                "units": "metric"
            }

            response = requests.get(base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data["name"],
                    "temp": round(data["main"]["temp"]),
                    "feels_like": round(data["main"]["feels_like"]),
                    "condition": data["weather"][0]["description"]
                }
        except Exception:
            continue

    return {"error": "City not found"}
