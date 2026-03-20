
import json
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Battery Dashboard API")

# Serve the static files (frontend)
# We will mount it at the end to catch all roots, but let's mount /static explicitly
app.mount("/static", StaticFiles(directory="static"), name="static")

BATTERY_DATA_FILE = "battery_data.json"
SETTINGS_FILE = "settings.json"

def load_battery_data():
    if not os.path.exists(BATTERY_DATA_FILE):
        return {}
    with open(BATTERY_DATA_FILE, "r") as f:
        return json.load(f)

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "power_draw_mode": "balanced"
        }
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.get("/api/data")
async def get_data():
    batteries = load_battery_data()
    settings = load_settings()
    
    return {
        "batteries": batteries,
        "settings": settings
    }

@app.post("/api/settings")
async def update_settings(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
        
    settings = load_settings()
    b_data = load_battery_data()
    
    if "power_draw_mode" in data:
        settings["power_draw_mode"] = data["power_draw_mode"]
            
    save_settings(settings)
    return {"status": "success", "settings": settings}

app.mount("/static", StaticFiles(directory="static"), name="static")