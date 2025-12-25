"""
Intelligent Cache Manager with LRU and TTL
Reduces redundant API calls by caching results
"""

import hashlib
import json
import time
from typing import Optional, Any, Dict
from collections import OrderedDict
from datetime import datetime, timedelta
import threading

class CacheManager:
    """
    LRU Cache with TTL (Time To Live) for API responses
    """
    
    def __init__(self, max_size: int = 100, ttl_seconds: int = 3600):
        """
        Initialize cache manager
        
        Args:
            max_size: Maximum number of cached entries
            ttl_seconds: Time to live for cache entries (default: 1 hour)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        
        # OrderedDict for LRU behavior
        self.cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        
        # Lock for thread safety
        self.lock = threading.Lock()
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def _generate_key(self, prompt: str, system_message: Optional[str] = None, **kwargs) -> str:
        """
        Generate cache key from prompt and parameters
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            **kwargs: Additional parameters
            
        Returns:
            Hash-based cache key
        """
        # Combine all inputs
        cache_input = {
            "prompt": prompt,
            "system_message": system_message or "",
            **kwargs
        }
        
        # Create deterministic JSON string
        cache_str = json.dumps(cache_input, sort_keys=True)
        
        # Generate hash
        return hashlib.sha256(cache_str.encode()).hexdigest()[:16]
    
    def get(self, prompt: str, system_message: Optional[str] = None, **kwargs) -> Optional[str]:
        """
        Get cached result if available and not expired
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            **kwargs: Additional parameters
            
        Returns:
            Cached result or None
        """
        key = self._generate_key(prompt, system_message, **kwargs)
        
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                
                # Check if expired
                if time.time() - entry["timestamp"] > self.ttl_seconds:
                    # Expired, remove from cache
                    del self.cache[key]
                    self.misses += 1
                    return None
                
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                
                # Cache hit
                self.hits += 1
                print(f"💾 Cache HIT (key: {key[:8]}...)")
                return entry["result"]
            
            # Cache miss
            self.misses += 1
            return None
    
    def set(self, result: str, prompt: str, system_message: Optional[str] = None, **kwargs):
        """
        Store result in cache
        
        Args:
            result: API response to cache
            prompt: User prompt
            system_message: Optional system message
            **kwargs: Additional parameters
        """
        key = self._generate_key(prompt, system_message, **kwargs)
        
        with self.lock:
            # Check if cache is full
            if len(self.cache) >= self.max_size and key not in self.cache:
                # Remove oldest entry (LRU)
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                self.evictions += 1
            
            # Store entry
            self.cache[key] = {
                "result": result,
                "timestamp": time.time()
            }
            
            print(f"💾 Cache SET (key: {key[:8]}..., size: {len(self.cache)}/{self.max_size})")
    
    def clear(self):
        """Clear all cache entries"""
        with self.lock:
            self.cache.clear()
            print("🗑️ Cache cleared")
    
    def cleanup_expired(self):
        """Remove expired entries from cache"""
        with self.lock:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self.cache.items()
                if current_time - entry["timestamp"] > self.ttl_seconds
            ]
            
            for key in expired_keys:
                del self.cache[key]
            
            if expired_keys:
                print(f"🗑️ Cleaned up {len(expired_keys)} expired cache entries")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        with self.lock:
            total_requests = self.hits + self.misses
            hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": f"{hit_rate:.1f}%",
                "evictions": self.evictions,
                "ttl_seconds": self.ttl_seconds
            }


# Global instance
cache_manager = CacheManager(max_size=100, ttl_seconds=3600)
