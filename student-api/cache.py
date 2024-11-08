import time
from threading import Lock
from typing import Optional, Dict, Any

class Cache:
    def __init__(self, duration: int = 300):
        self.cache: Dict[int, Dict[str, Any]] = {}
        self.cache_duration = duration
        self.lock = Lock()  # To ensure thread safety when accessing/modifying the cache

    def cleanup(self) -> None:
        """Remove expired cache entries."""
        current_time = time.time()
        with self.lock:
            expired = [
                k for k, v in self.cache.items()
                if current_time - v['timestamp'] > self.cache_duration
            ]
            for k in expired:
                del self.cache[k]

    def get(self, key: int, prompt: str) -> Optional[str]:
        """Retrieve summary from the cache if it exists and is not expired."""
        self.cleanup()  # Cleanup expired entries before getting the value
        with self.lock:
            if key in self.cache:
                cached = self.cache[key]
                if cached['prompt'] == prompt and \
                   time.time() - cached['timestamp'] < self.cache_duration:
                    return cached['summary']
        return None

    def set(self, key: int, prompt: str, summary: str) -> None:
        """Store summary in the cache with the current timestamp."""
        with self.lock:
            self.cache[key] = {
                'prompt': prompt,
                'summary': summary,
                'timestamp': time.time()
            }

_cache = Cache()

def cache_summary(student_id: int, prompt: str, summary: Optional[str] = None) -> Optional[str]:
    """Set or get summary for a student, handling concurrency safely."""
    if summary:
        _cache.set(student_id, prompt, summary)
        return summary
    return _cache.get(student_id, prompt)
