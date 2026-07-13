import json
import asyncio
import numpy as np
import logging
from typing import Optional, Any, List, Tuple
from config.settings import get_settings

logger = logging.getLogger("semantic_cache")

class SemanticCacheManager:
    def __init__(self, threshold: float = 0.95):
        self.threshold = threshold
        # In-memory store of (embedding, response). In production, this would be a Vector DB.
        self.cache: List[Tuple[np.ndarray, Any]] = []
        self.lock = asyncio.Lock()

    async def get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Gets the embedding for a given text using Gemini API."""
        try:
            from google import genai
            settings = get_settings()
            
            raw_keys = settings.GEMINI_API_KEYS
            keys = [k.strip() for k in raw_keys.split(",") if k.strip()]
            if not keys:
                return None
            
            # Use the first key for embedding generation
            client = genai.Client(api_key=keys[0])
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: client.models.embed_content(
                    model='gemini-embedding-2',
                    contents=text
                )
            )
            # result is an EmbedContentResponse, which has embeddings list
            # Each embedding has a values list
            return np.array(result.embeddings[0].values)
        except Exception as e:
            logger.warning(f"Failed to generate embedding for intent cache: {e}")
            return None

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return np.dot(a, b) / (norm_a * norm_b)

    async def get_semantic(self, prompt: str) -> Optional[Any]:
        """Checks if a semantically similar prompt has been cached based on intent."""
        async with self.lock:
            if not self.cache:
                return None
                
        emb = await self.get_embedding(prompt)
        if emb is None:
            return None
            
        async with self.lock:
            best_sim = 0.0
            best_response = None
            
            for cached_emb, response in self.cache:
                sim = self._cosine_similarity(emb, cached_emb)
                if sim > best_sim:
                    best_sim = sim
                    best_response = response
                    
            if best_sim >= self.threshold:
                logger.info(f"Intent-based semantic cache HIT! (Similarity: {best_sim:.4f})")
                return best_response
                
        return None

    async def set_semantic(self, prompt: str, response: Any):
        """Saves a prompt and its response to the intent-based semantic cache."""
        emb = await self.get_embedding(prompt)
        if emb is not None:
            async with self.lock:
                self.cache.append((emb, response))
                logger.info("Added new response to intent-based semantic cache.")

semantic_cache_manager = SemanticCacheManager(threshold=0.96)
