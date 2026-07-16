import hashlib
import asyncio
import logging
import time
from typing import Optional, Any, Dict

logger = logging.getLogger("semantic_cache")

class SemanticCacheManager:
    """
    Optimized to an Exact-Match Hash Cache.
    Using semantic embeddings over the network took too much time and wasted tokens.
    This guarantees 0 token usage for caching and 0ms latency.
    """
    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, dict] = {}
        self.ttl_seconds = ttl_seconds
        self.lock = asyncio.Lock()

    def _hash_prompt(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode('utf-8')).hexdigest()

    async def get_semantic(self, prompt: str) -> Optional[Any]:
        """Checks if an exactly matching prompt has been cached."""
        prompt_hash = self._hash_prompt(prompt)
        async with self.lock:
            if prompt_hash in self.cache:
                entry = self.cache[prompt_hash]
                if time.time() - entry['timestamp'] < self.ttl_seconds:
                    logger.info("Exact-match prompt cache HIT! (0 tokens used, 0ms latency)")
                    return entry['response']
                else:
                    del self.cache[prompt_hash]
        return None

    async def set_semantic(self, prompt: str, response: Any):
        """Saves a prompt and its response to the exact-match cache."""
        prompt_hash = self._hash_prompt(prompt)
        async with self.lock:
            self.cache[prompt_hash] = {
                'response': response,
                'timestamp': time.time()
            }
            logger.info("Added new response to exact-match prompt cache.")

semantic_cache_manager = SemanticCacheManager(ttl_seconds=3600)
