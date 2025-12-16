import os
import re
import requests
from dotenv import load_dotenv
from tools.weather_tool import get_weather

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "WeatherMind Agent"
}

# -------------------- LLM CALL --------------------

def call_llm(prompt: str, temperature: float = 0.4) -> str:
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=HEADERS,
        json=payload,
        timeout=20
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def is_country_llm(name: str) -> bool:
    prompt = f"""
    Is "{name}" a COUNTRY (not a city)?

    Respond ONLY with YES or NO.
    """
    try:
        result = call_llm(prompt, temperature=0).strip().upper()
        return result == "YES"
    except Exception:
        return False


# -------------------- CITY EXTRACTION (FINAL & GUARANTEED) --------------------

def extract_city(query: str) -> str:
    """
    Robust city extraction:
    1. LLM attempt
    2. Smart deterministic fallback (NO last-word bug)
    """

    # 🟢 1️⃣ LLM ATTEMPT
    prompt = f"""
    The user is asking about weather.

    Extract the CITY NAME mentioned in the input.
    - City can be anywhere in the world
    - Ignore weather words, time words, and conditions
    - Respond ONLY with the city name
    - If no city is mentioned, respond with NONE

    User input:
    "{query}"
    """

    try:
        city = call_llm(prompt, temperature=0).strip()
        if city and city.upper() != "NONE":
            city = re.sub(r"[^\w\s]", "", city)
            city = re.sub(r"\s+", " ", city).strip()
            if len(city) >= 3:
                return city.title()
    except Exception:
        pass

    # 🟡 2️⃣ SMART FALLBACK (POSITION-BASED)

    q = query.lower()

    # Common patterns: "pune me", "in london", "of delhi"
    match = re.search(r"(?:in|of|me|mein|मधे)\s+([a-zA-Z]{3,})", q)
    if match:
        return match.group(1).title()

    # 🟠 3️⃣ SAFE TOKEN FALLBACK (IGNORE STOP WORDS)
    stop_words = {
        "aaj", "kal", "ka", "ki", "ke", "hai", "kya",
        "mausam", "weather", "kaisa", "kaisi", "kaise",
        "today", "how", "is"
    }

    tokens = re.findall(r"\b[a-zA-Z]{3,}\b", q)
    tokens = [t for t in tokens if t not in stop_words]

    if tokens:
        return tokens[0].title()   # 👈 FIRST meaningful token, NOT last

    return ""


# -------------------- RESPONSE FORMATTER (CHATGPT-LIKE) --------------------

def format_response(query: str, weather: dict) -> str:
    prompt = f"""
    You are a helpful assistant like ChatGPT.

    VERY IMPORTANT:
    - Reply in EXACTLY the same language, script, and tone as the user's input
    - If user uses Hinglish, reply in Hinglish
    - If user uses Hindi, reply in Hindi
    - If user uses English, reply in English
    - Do NOT switch language
    - Be short, natural, and human-like
    - Do NOT translate city names
    - Do NOT change numbers

    User input:
    "{query}"

    Weather data:
    City: {weather['city']}
    Temperature: {weather['temp']}°C
    Feels like: {weather['feels_like']}°C
    Condition: {weather['condition']}
    """

    try:
        return call_llm(prompt, temperature=0.5)
    except Exception:
        return (
            f"The current temperature in {weather['city']} is "
            f"{weather['temp']}°C with {weather['condition']}."
        )



# -------------------- MAIN AGENT (FINAL FLOW) --------------------

def run_weather_agent(query: str) -> str:
    if not query or not isinstance(query, str):
        return "Please ask a valid weather question."

    # 1️⃣ Extract city
    city = extract_city(query)

    if not city:
        return "Sorry, I couldn't understand which city's weather you want."

    # 🚨 COUNTRY HANDLING (CRITICAL FIX)
    if is_country_llm(city):
        return format_response(
            query,
            {
                "city": "",
                "temp": "N/A",
                "feels_like": "N/A",
                "condition": "a country name"
            }
        )

    # 2️⃣ Weather API
    weather = get_weather(city)

    if not isinstance(weather, dict) or "error" in weather:
        return f"Sorry, I couldn't fetch live weather for {city}."

    # 3️⃣ Language-mirrored response
    return format_response(query, weather)
