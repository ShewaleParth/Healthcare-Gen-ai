


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import hospital, diagnosis, treatment, mental_health
from app.config import Config
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Perform startup validation
Config.startup_check()

app = FastAPI(
    title="Aarogya AI - Healthcare Intelligence System",
    description="Multi-agent AI system for diagnostics, treatment, mental health & hospital optimization",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "running", "message": "GenAI Hackathon Backend is live"}

@app.get("/health")
def health_check():
    return {"service": "backend", "health": "ok"}

# Register API Routers
app.include_router(hospital.router, prefix="/api/v1/hospital", tags=["Hospital"])
app.include_router(diagnosis.router, prefix="/api/v1/diagnostic", tags=["Diagnostic"])
app.include_router(treatment.router, prefix="/api/v1/treatment", tags=["Treatment"])
app.include_router(mental_health.router, prefix="/api/v1/mental-health", tags=["Mental Health"])

