from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.weather_agent import run_weather_agent

app = FastAPI(title="WeatherMind API")

# 🔥 ADD THIS (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body structure
class ChatRequest(BaseModel):
    message: str

# Response body structure
class ChatResponse(BaseModel):
    reply: str

# Health check (optional but good)
@app.get("/")
def root():
    return {"status": "WeatherMind API running"}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = run_weather_agent(request.message)
    return {"reply": reply}
