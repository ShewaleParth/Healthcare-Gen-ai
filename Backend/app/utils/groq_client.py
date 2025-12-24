"""
Groq API Client Wrapper with Error Handling and Rate Limiting
Provides a robust interface to Groq API with retry logic and fallbacks
"""

from groq import Groq
from app.config import Config
import time
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class GroqClient:
    """Enhanced Groq client with error handling and rate limiting"""
    
    def __init__(self):
        """Initialize Groq client with configuration"""
        if not Config.GROQ_API_KEY:
            raise ValueError("Groq API key not configured")
        
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.primary_model = Config.PRIMARY_MODEL
        self.fallback_model = Config.FALLBACK_MODEL
        self.request_count = 0
        self.last_request_time = time.time()
    
    def _check_rate_limit(self):
        """Simple rate limit check"""
        current_time = time.time()
        time_diff = current_time - self.last_request_time
        
        # Reset counter every minute
        if time_diff >= 60:
            self.request_count = 0
            self.last_request_time = current_time
        
        # Check if we're at limit
        if self.request_count >= Config.MAX_REQUESTS_PER_MINUTE:
            wait_time = 60 - time_diff
            if wait_time > 0:
                logger.warning(f"Rate limit reached. Waiting {wait_time:.1f}s")
                time.sleep(wait_time)
                self.request_count = 0
                self.last_request_time = time.time()
    
    def chat_completion(
        self,
        messages: list,
        agent_type: str = "general",
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create chat completion with error handling and retries
        
        Args:
            messages: List of message dicts
            agent_type: Type of agent (for temperature override)
            model: Override model (optional)
            **kwargs: Additional parameters
        
        Returns:
            Dict with response or error
        """
        # Check rate limit
        self._check_rate_limit()
        
        # Get model configuration
        model_config = Config.get_model_config(agent_type)
        
        # Use provided model or default
        selected_model = model or self.primary_model
        
        # Merge configurations
        params = {
            "model": selected_model,
            "messages": messages,
            "temperature": model_config.get("temperature", 0.3),
            "max_tokens": model_config.get("max_tokens", 2500),
            "top_p": model_config.get("top_p", 0.9),
            **kwargs
        }
        
        # Retry logic
        for attempt in range(Config.MAX_RETRIES):
            try:
                # Make API call
                response = self.client.chat.completions.create(**params)
                
                # Increment counter
                self.request_count += 1
                
                # Return successful response
                return {
                    "success": True,
                    "content": response.choices[0].message.content,
                    "model": selected_model,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                }
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Attempt {attempt + 1} failed: {error_msg}")
                
                # Check if it's a rate limit error
                if "rate_limit" in error_msg.lower():
                    if attempt < Config.MAX_RETRIES - 1:
                        wait_time = Config.RETRY_DELAY * (Config.BACKOFF_FACTOR ** attempt)
                        logger.info(f"Rate limited. Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        return {
                            "success": False,
                            "error": "rate_limit",
                            "message": Config.ERROR_MESSAGES["rate_limit"]
                        }
                
                # Try fallback model on last attempt
                if attempt == Config.MAX_RETRIES - 1 and selected_model == self.primary_model:
                    logger.info(f"Trying fallback model: {self.fallback_model}")
                    params["model"] = self.fallback_model
                    try:
                        response = self.client.chat.completions.create(**params)
                        self.request_count += 1
                        return {
                            "success": True,
                            "content": response.choices[0].message.content,
                            "model": self.fallback_model,
                            "fallback": True,
                            "usage": {
                                "prompt_tokens": response.usage.prompt_tokens,
                                "completion_tokens": response.usage.completion_tokens,
                                "total_tokens": response.usage.total_tokens
                            }
                        }
                    except Exception as fallback_error:
                        logger.error(f"Fallback model also failed: {fallback_error}")
                
                # Wait before retry
                if attempt < Config.MAX_RETRIES - 1:
                    wait_time = Config.RETRY_DELAY * (Config.BACKOFF_FACTOR ** attempt)
                    time.sleep(wait_time)
        
        # All retries failed
        return {
            "success": False,
            "error": "api_error",
            "message": Config.ERROR_MESSAGES["model_error"],
            "details": error_msg
        }

# Global client instance
groq_client = GroqClient() if Config.validate_api_key() else None
