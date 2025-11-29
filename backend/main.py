"""
EcoTrack AI Backend - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="EcoTrack AI API",
    description="Personal Carbon Footprint Tracker API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "EcoTrack AI API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Import routers
from routers import activities, emissions, recommendations

app.include_router(activities.router, prefix="/activity", tags=["activities"])
app.include_router(emissions.router, prefix="/emissions", tags=["emissions"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

