from threading import Lock
import time
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class Cache:
    def __init__(self, duration: int = 300):
        self.cache: Dict[int, Dict[str, Any]] = {}
        self.cache_duration = duration
        self.lock = Lock()
        self.stats = {"hits": 0, "misses": 0, "evictions": 0}

    def cleanup(self) -> None:
        current_time = time.time()
        with self.lock:
            expired = [
                k for k, v in self.cache.items()
                if current_time - v['timestamp'] > self.cache_duration
            ]
            for k in expired:
                del self.cache[k]
                self.stats["evictions"] += 1

    def get(self, key: int, prompt: str) -> Optional[str]:
        self.cleanup()
        with self.lock:
            if key in self.cache:
                cached = self.cache[key]
                if cached['prompt'] == prompt and \
                   time.time() - cached['timestamp'] < self.cache_duration:
                    self.stats["hits"] += 1
                    return cached['summary']
            self.stats["misses"] += 1
            return None

    def set(self, key: int, prompt: str, summary: str) -> None:
        with self.lock:
            self.cache[key] = {
                'prompt': prompt,
                'summary': summary,
                'timestamp': time.time()
            }

    def get_stats(self) -> Dict[str, Any]:
        with self.lock:
            total = self.stats["hits"] + self.stats["misses"]
            return {
                **self.stats,
                "size": len(self.cache),
                "hit_rate": self.stats["hits"] / total if total > 0 else 0
            }

_cache = Cache()


def cache_summary(student_id: int, prompt: str, summary: Optional[str] = None) -> Optional[str]:
    if summary:
        _cache.set(student_id, prompt, summary)
        return summary
    return _cache.get(student_id, prompt)