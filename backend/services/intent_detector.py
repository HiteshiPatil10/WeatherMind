def is_weather_query(message: str) -> bool:
    """
    Simple intent detection to check if user is asking about weather
    """
    message = message.lower()

    weather_keywords = [
        "weather",
        "temperature",
        "temp",
        "rain",
        "climate",
        "forecast",
        "hot",
        "cold",
        "humidity"
    ]

    return any(keyword in message for keyword in weather_keywords)
