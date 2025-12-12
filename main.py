from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from model_loader import generate_text
import json
import os
from dotenv import load_dotenv

# Using .env file to load the key before start of the app
load_dotenv()

# API_KEY variable got from .env
API_KEY = os.getenv("API_KEY")

if not API_KEY: 
    raise ValueError("API_KEY is not set in the file .env.")

# Default values for mock if ESP-32 is not connected
DEFAULT_SENSOR_DATA = {
    "avg_temp_C": 55.0,
    "avg_humidity_percent": 50.0,
    "mq1_percent": 15.0,
    "mq2_percent": 5.0          
}

# Definition of the App
app = FastAPI(title="ESP32 Sensor + Chatbot API with API Key")

# Cached latest sensor data received
sensor_data = {}
sensor_data = DEFAULT_SENSOR_DATA.copy()

# User chat request class
class ChatRequest(BaseModel):
    user_message: str

# Check if API key is valid  
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# ENDPOINTS

# Simple check server is up
@app.get("/")
async def root():
    return {"message": "ESP32 + Chatbot API with API Key is running!"}

# Route used by ESP-32 to send sensors data to server
@app.post("/sensor-data")
async def receive_sensor_data(data: dict, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    global sensor_data
    sensor_data = data
    return {"status": "ok", "received_keys": list(sensor_data.keys())}

# Route to send 
@app.get("/latest-data")
async def get_latest_sensor_data(x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    global sensor_data
    
    if not sensor_data:
        return {
            "avg_temp_C": 0.0,
            "avg_humidity_percent": 0.0,
            "mq1_percent": 0.0,
            "mq2_percent": 0.0
        }
        
    return sensor_data

# Chat route where the client user prompt is combined with a predefined prompt and the sensors data
@app.post("/chat")
async def chat(req: ChatRequest, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    
    sensor_data_str = json.dumps(sensor_data) if isinstance(sensor_data, dict) else str(sensor_data)

    prompt = (


        "TASK: You are Compost Master 5000, an AI expert. Analyze sensor data ONLY and provide concise, actionable advice (e.g., 'Add water', 'Turn the pile').\n\n"

        "Optimal Ranges:\n"

        f"Temp: 55-65°C (Crit: <40°C Cool | >70°C Hot)\n"

        f"Moisture: 40-60% (Crit: <40% Dry | >65% Wet)\n"

        f"Aeration (MQ): High MQ1/MQ2 (>800) suggests anaerobic decay (Needs Oxygen).\n\n"


        f"DATA:\n{sensor_data_str}\n"

        f"QUERY: {req.user_message}\n\n"


        "Based on DATA and Optimal Ranges, provide ONLY a single, actionable instruction or brief status.\n"

        "ACTIONABLE ADVICE: "
    )
    
    raw_reply = generate_text(prompt)
    
    MARKER = "ACTIONABLE ADVICE: "
    
    if MARKER in raw_reply:
        final_reply = raw_reply.split(MARKER, 1)[-1].strip()
    else:
        final_reply = raw_reply.strip() 
        
    return {"response": final_reply}