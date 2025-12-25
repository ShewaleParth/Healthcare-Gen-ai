"""
Global Rate Limiter with Token Bucket Algorithm and Semaphore Queue
Prevents API flooding and manages concurrent requests
"""

import time
import threading
from collections import deque
from typing import Optional
from datetime import datetime, timedelta

class RateLimiter:
    """
    Token bucket rate limiter with semaphore for concurrent call control
    """
    
    def __init__(self, calls_per_minute: int = 60, max_concurrent: int = 5):
        """
        Initialize rate limiter
        
        Args:
            calls_per_minute: Maximum API calls per minute
            max_concurrent: Maximum concurrent API calls
        """
        self.calls_per_minute = calls_per_minute
        self.max_concurrent = max_concurrent
        
        # Token bucket for rate limiting
        self.tokens = calls_per_minute
        self.max_tokens = calls_per_minute
        self.last_refill = time.time()
        self.refill_rate = calls_per_minute / 60.0  # tokens per second
        
        # Semaphore for concurrent call limiting
        self.semaphore = threading.Semaphore(max_concurrent)
        
        # Call history for monitoring
        self.call_history = deque(maxlen=100)
        
        # Lock for thread safety
        self.lock = threading.Lock()
        
        # Backoff state
        self.backoff_until = None
        self.consecutive_failures = 0
    
    def _refill_tokens(self):
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill
        
        # Add tokens based on elapsed time
        new_tokens = elapsed * self.refill_rate
        self.tokens = min(self.max_tokens, self.tokens + new_tokens)
        self.last_refill = now
    
    def acquire(self, timeout: float = 30.0) -> bool:
        """
        Acquire permission to make an API call
        
        Args:
            timeout: Maximum time to wait for permission (seconds)
            
        Returns:
            True if permission granted, False if timeout
        """
        start_time = time.time()
        
        # Check if in backoff period
        if self.backoff_until:
            wait_time = (self.backoff_until - datetime.now()).total_seconds()
            if wait_time > 0:
                print(f"⏳ Rate limiter in backoff mode, waiting {wait_time:.1f}s...")
                if wait_time > timeout:
                    return False
                time.sleep(wait_time)
                self.backoff_until = None
        
        # Try to acquire semaphore (concurrent call limit)
        if not self.semaphore.acquire(timeout=timeout):
            print("⚠️ Too many concurrent requests, please wait...")
            return False
        
        try:
            # Wait for token availability
            while True:
                with self.lock:
                    self._refill_tokens()
                    
                    if self.tokens >= 1.0:
                        # Token available, consume it
                        self.tokens -= 1.0
                        self.call_history.append(time.time())
                        return True
                
                # Check timeout
                if time.time() - start_time > timeout:
                    print("⚠️ Rate limit timeout, request denied")
                    return False
                
                # Wait a bit before retrying
                time.sleep(0.1)
        
        except Exception as e:
            # Release semaphore on error
            self.semaphore.release()
            raise e
    
    def release(self):
        """Release the semaphore after API call completes"""
        self.semaphore.release()
    
    def report_success(self):
        """Report successful API call"""
        with self.lock:
            self.consecutive_failures = 0
    
    def report_rate_limit_error(self):
        """Report rate limit error and activate backoff"""
        with self.lock:
            self.consecutive_failures += 1
            
            # Exponential backoff: 2^failures seconds (max 60s)
            backoff_seconds = min(2 ** self.consecutive_failures, 60)
            self.backoff_until = datetime.now() + timedelta(seconds=backoff_seconds)
            
            print(f"🚨 Rate limit detected! Backing off for {backoff_seconds}s (failure #{self.consecutive_failures})")
    
    def get_stats(self) -> dict:
        """Get rate limiter statistics"""
        with self.lock:
            recent_calls = len([t for t in self.call_history if time.time() - t < 60])
            
            return {
                "tokens_available": int(self.tokens),
                "max_tokens": self.max_tokens,
                "calls_last_minute": recent_calls,
                "calls_per_minute_limit": self.calls_per_minute,
                "max_concurrent": self.max_concurrent,
                "consecutive_failures": self.consecutive_failures,
                "in_backoff": self.backoff_until is not None
            }


class RateLimiterManager:
    """Manages separate rate limiters for different APIs"""
    
    def __init__(self):
        # Google Gemini: 60 calls/min, max 5 concurrent
        self.google_limiter = RateLimiter(calls_per_minute=60, max_concurrent=5)
        
        # Grok: 100 calls/min, max 10 concurrent
        self.grok_limiter = RateLimiter(calls_per_minute=100, max_concurrent=10)
    
    def get_limiter(self, api_name: str) -> RateLimiter:
        """Get rate limiter for specific API"""
        if api_name.lower() in ['google', 'gemini']:
            return self.google_limiter
        elif api_name.lower() in ['grok', 'xai']:
            return self.grok_limiter
        else:
            raise ValueError(f"Unknown API: {api_name}")
    
    def get_all_stats(self) -> dict:
        """Get statistics for all rate limiters"""
        return {
            "google": self.google_limiter.get_stats(),
            "grok": self.grok_limiter.get_stats()
        }


# Global instance
rate_limiter_manager = RateLimiterManager()
