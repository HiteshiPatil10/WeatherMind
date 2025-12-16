# WeatherMind

A full-stack Agentic AI system that reasons over user intent and uses tools to deliver transparent, real-world weather insights.

## Features
- Natural-language weather queries in English, Hindi, and Hinglish.
- LLM-driven city extraction and response generation
- Real-time weather data using OpenWeather API
- Agentic architecture (LLM + Tool)
- OpenRouter used as LLM gateway
- Live weather from OpenWeatherMap.
- Small React frontend for quick demo and a FastAPI backend.

## 🧠 Architecture
1. User enters a weather-related query
2. LLM extracts the city from the query
3. Weather tool fetches live weather data
4. LLM formats a natural language response
5. Response is returned via FastAPI backend

## 🛠 Tech Stack
- **Backend:** Python, FastAPI
- **LLM:** OpenRouter (Groq LLaMA model)
- **Weather API:** OpenWeather
- **Frontend:** React + Tailwind CSS
- **Agent Logic:** Tool-based LLM reasoning

## Quick start

1. Backend
   - Create a Python virtual environment and install dependencies:
     ```sh
     python -m venv venv
     venv\Scripts\activate   # Windows
     pip install -r backend/requirements.txt
     ```
   - Add keys to [.env](http://_vscodecontentref_/0) (see below) then run:
     ```sh
     uvicorn backend.main:app --reload --port 8000
     ```

2. Frontend
   - From the [frontend](http://_vscodecontentref_/1) folder:
     ```sh
     cd frontend
     npm install
     npm start
     ```
   - Open http://localhost:3000

## Environment variables
Set the following in [.env](http://_vscodecontentref_/2) (already present in project for local dev but replace with your own keys):
- WEATHER_API_KEY — OpenWeatherMap API key
- OPENROUTER_API_KEY — LLM provider key
- OPENROUTER_MODEL — LLM model id
- GROQ_API_KEY / GROQ_MODEL — optional (used by groq_test)

See [.env](http://_vscodecontentref_/3) for example entries.

## Project structure (important files)
- Backend API: [main.py](http://_vscodecontentref_/4) — exposes POST /chat (function: [main.chat](http://_vscodecontentref_/5))
- Agent logic: [weather_agent.py](http://_vscodecontentref_/6) — city extraction, LLM calls, formatting (entry: [agents.weather_agent.run_weather_agent](http://_vscodecontentref_/7))
- Weather tool: [weather_tool.py](http://_vscodecontentref_/8) — live fetch from OpenWeatherMap (function: [tools.weather_tool.get_weather](http://_vscodecontentref_/9))
- Intent helper: [intent_detector.py](http://_vscodecontentref_/10) — simple weather intent check ([services.intent_detector.is_weather_query](http://_vscodecontentref_/11))
- Frontend: [App.js](http://_vscodecontentref_/12) — simple UI calling backend
- Frontend config: [package.json](http://_vscodecontentref_/13)

## How it works (high-level)
1. Frontend sends user text to backend `/chat`.
2. Backend runs [run_weather_agent](http://_vscodecontentref_/14) which:
   - Extracts a city (LLM-first, deterministic fallback)
   - Detects if input is a country (LLM)
   - Calls [get_weather](http://_vscodecontentref_/15) to fetch live weather
   - Formats reply via LLM or returns a fallback string
3. Frontend displays the reply.

## Development notes
- CORS is enabled in [main.py](http://_vscodecontentref_/16) to allow the frontend at http://localhost:3000.
- Tests: frontend has basic jest setup ([setupTests.js](http://_vscodecontentref_/17)) and a sample test ([App.test.js](http://_vscodecontentref_/18)).
- Replace any demo API keys in [.env](http://_vscodecontentref_/19) before sharing or deploying.

## Contributing
- Open an issue for bugs or features.
- Follow the existing code style and run the frontend/backend locally to verify behavior.

## License
MIT — see
