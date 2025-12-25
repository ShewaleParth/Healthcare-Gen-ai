
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import hospital, diagnostic, treatment, mental_health, user_health
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="GenAI Healthcare Copilot",
    description="Agentic AI backend for diagnostics, treatment & hospital optimization",
    version="1.0.0"
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
app.include_router(diagnostic.router, prefix="/api/v1/diagnostic", tags=["Diagnostic"])
app.include_router(treatment.router, prefix="/api/v1/treatment", tags=["Treatment"])
app.include_router(mental_health.router, prefix="/api/v1/mental-health", tags=["Mental Health"])
app.include_router(user_health.router, prefix="/api/v1/user", tags=["User Health"])

