"""
Centralized Configuration for Aarogya AI Backend
Manages API keys, model selection, rate limits, and environment settings
"""

import os
from dotenv import load_dotenv
from typing import Optional
import sys

# Load environment variables
load_dotenv()

class Config:
    """Central configuration management"""
    
    # ============================================
    # API CONFIGURATION
    # ============================================
    
    # Groq API Key (using GOOGLE_API_KEY for compatibility)
    GROQ_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Validate API key on import
    @staticmethod
    def validate_api_key() -> bool:
        """Validate that API key is configured"""
        if not Config.GROQ_API_KEY or Config.GROQ_API_KEY == "your_groq_api_key_here":
            return False
        if not Config.GROQ_API_KEY.startswith("gsk_"):
            print("⚠️  Warning: API key doesn't start with 'gsk_' - may be invalid")
            return False
        return True
    
    # ============================================
    # MODEL CONFIGURATION
    # ============================================
    
    # Primary model for all agents (best free tier option)
    PRIMARY_MODEL = "llama-3.3-70b-versatile"
    
    # Fallback model (if primary fails)
    FALLBACK_MODEL = "llama-3.1-70b-versatile"
    
    # Model-specific settings
    MODEL_SETTINGS = {
        "llama-3.3-70b-versatile": {
            "max_tokens": 2500,
            "temperature": 0.3,  # Lower for medical accuracy
            "top_p": 0.9,
            "description": "Latest Llama 3.3 - Best for medical applications"
        },
        "llama-3.1-70b-versatile": {
            "max_tokens": 2000,
            "temperature": 0.3,
            "top_p": 0.9,
            "description": "Llama 3.1 - Reliable fallback"
        }
    }
    
    # Agent-specific temperature overrides
    AGENT_TEMPERATURES = {
        "diagnostic": 0.2,      # Very low for consistent medical analysis
        "treatment": 0.2,       # Very low for safe recommendations
        "mental_health": 0.7,   # Higher for empathetic responses
        "hospital": 0.3         # Moderate for data analysis
    }
    
    # ============================================
    # RATE LIMITING (Groq Free Tier)
    # ============================================
    
    MAX_REQUESTS_PER_MINUTE = 30
    MAX_TOKENS_PER_MINUTE = 20_000
    
    # Request timeout (seconds)
    REQUEST_TIMEOUT = 30
    
    # Retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    BACKOFF_FACTOR = 2  # exponential backoff
    
    # ============================================
    # OPTIONAL: GOOGLE CLOUD (Production)
    # ============================================
    
    GCP_PROJECT_ID: Optional[str] = os.getenv("GCP_PROJECT_ID")
    GCP_LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
    BIGQUERY_DATASET: str = os.getenv("BIGQUERY_DATASET", "aarogya_healthcare")
    GCS_BUCKET: Optional[str] = os.getenv("GCS_BUCKET")
    
    # ============================================
    # APPLICATION SETTINGS
    # ============================================
    
    # Environment
    ENV = os.getenv("ENV", "development")
    DEBUG = ENV == "development"
    
    # File upload settings
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES = ["image/png", "image/jpeg", "image/jpg"]
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # ============================================
    # ERROR MESSAGES
    # ============================================
    
    ERROR_MESSAGES = {
        "no_api_key": """
❌ Groq API Key not configured!

To fix this:
1. Visit https://console.groq.com
2. Sign up (free, no credit card required)
3. Create an API key
4. Add to .env file: GOOGLE_API_KEY=gsk_your_key_here
5. Restart the backend server

Current .env location: Backend/.env
""",
        "invalid_api_key": """
❌ Invalid Groq API Key!

Your API key should:
- Start with 'gsk_'
- Be obtained from https://console.groq.com
- Be kept secret (never commit to Git)

Please check your .env file.
""",
        "rate_limit": """
⚠️ Rate limit exceeded!

Groq free tier limits:
- 30 requests per minute
- 20,000 tokens per minute

Please wait a moment and try again.
""",
        "model_error": """
❌ Model error occurred!

This could be due to:
- API key issues
- Network connectivity
- Groq service availability

Please check your API key and try again.
"""
    }
    
    @staticmethod
    def get_model_config(agent_type: str) -> dict:
        """Get optimized model configuration for specific agent"""
        base_config = Config.MODEL_SETTINGS[Config.PRIMARY_MODEL].copy()
        
        # Override temperature for specific agent
        if agent_type in Config.AGENT_TEMPERATURES:
            base_config["temperature"] = Config.AGENT_TEMPERATURES[agent_type]
        
        return base_config
    
    @staticmethod
    def startup_check():
        """Perform startup validation"""
        print("\n" + "="*60)
        print("🏥 AAROGYA AI - BACKEND STARTUP")
        print("="*60)
        
        # Check API key
        if not Config.validate_api_key():
            print(Config.ERROR_MESSAGES["no_api_key"])
            if not Config.DEBUG:
                sys.exit(1)
            else:
                print("⚠️  Running in DEBUG mode without API key")
        else:
            print(f"✅ API Key configured: {Config.GROQ_API_KEY[:15]}...")
        
        # Show model info
        print(f"✅ Primary Model: {Config.PRIMARY_MODEL}")
        print(f"✅ Fallback Model: {Config.FALLBACK_MODEL}")
        
        # Show rate limits
        print(f"✅ Rate Limit: {Config.MAX_REQUESTS_PER_MINUTE} req/min")
        
        # Show environment
        print(f"✅ Environment: {Config.ENV}")
        
        print("="*60 + "\n")
        
        return Config.validate_api_key()

# Validate on import (only in production)
if Config.ENV == "production":
    if not Config.validate_api_key():
        print(Config.ERROR_MESSAGES["no_api_key"])
        sys.exit(1)
