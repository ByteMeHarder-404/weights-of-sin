"""Simple in-memory cache service with TTL support."""

import time
from typing import Dict, Any, Optional, Tuple

class Cache:
    def __init__(self, ttl_seconds: int = 3600):
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self.ttl_seconds = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache if it exists and hasn't expired."""
        if key not in self._cache:
            return None
        
        value, timestamp = self._cache[key]
        if time.time() - timestamp > self.ttl_seconds:
            del self._cache[key]
            return None
            
        return value

    def set(self, key: str, value: Any):
        """Set a value in cache with current timestamp."""
        self._cache[key] = (value, time.time())

    def clear(self):
        """Clear all cached values."""
        self._cache.clear()

# Create cache instances with different TTLs
journal_cache = Cache(ttl_seconds=3600)  # 1 hour for journal data
author_cache = Cache(ttl_seconds=7200)   # 2 hours for author data
abstract_cache = Cache(ttl_seconds=1800)  # 30 minutes for abstracts