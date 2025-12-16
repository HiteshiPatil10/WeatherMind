import requests
import os
from dotenv import load_dotenv
load_dotenv()
def get_weather(city: str) -> str:
    """
    Fetches current weather for a given city using OpenWeather API
    """
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        return "Weather API key not configured."

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return f"Could not find weather for {city}."

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]

        return f"The weather in {city} is {temp}°C with {description}."

    except Exception as e:
        return "Error fetching weather data."
