from redis import Redis
from functools import wraps
import json
from typing import Any, Callable, Optional

redis_client = Redis(host='redis', port=6379, db=0)

def cache(ttl: int = 300):  # default TTL 5 minutes
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Generate cache key
            key = f"{func.__name__}:{str(args)}_{str(kwargs)}"
            
            # Try to get from cache
            cached_data = redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
            
            # If not in cache, execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            redis_client.setex(key, ttl, json.dumps(result))
            
            return result
        return wrapper
    return decorator

def invalidate_cache(pattern: str) -> None:
    """Invalidate all cache keys matching the pattern"""
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key) 