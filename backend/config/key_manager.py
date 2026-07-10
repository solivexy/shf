import asyncio
import time
import json
import logging
from typing import List, Optional, Dict, Any, Union
from config.settings import get_settings

logger = logging.getLogger("key_manager")


class APIKeyManager:
    """
    Manages a pool of Google Gemini API keys with automatic rotation and cooldown handling.
    If one key reaches rate limit (HTTP 429 / ResourceExhausted), it rotates to the next available key.
    """
    def __init__(self, api_keys_str: Optional[str] = None):
        settings = get_settings()
        raw_keys = api_keys_str if api_keys_str is not None else settings.GEMINI_API_KEYS
        self.keys: List[str] = [k.strip() for k in raw_keys.split(",") if k.strip()] if raw_keys else []
        self.cooldowns: Dict[str, float] = {key: 0.0 for key in self.keys}
        self.current_index: int = 0
        self.lock = asyncio.Lock()
        self.model_name = settings.GEMINI_MODEL

    async def get_active_key(self) -> Optional[str]:
        """Returns the next available API key not on cooldown."""
        if not self.keys:
            return None

        async with self.lock:
            now = time.time()
            # Try finding a key not on cooldown
            for _ in range(len(self.keys)):
                key = self.keys[self.current_index]
                if self.cooldowns[key] <= now:
                    # Key is ready
                    self.current_index = (self.current_index + 1) % len(self.keys)
                    return key
                self.current_index = (self.current_index + 1) % len(self.keys)

            # If all keys are on cooldown, return the one that expires earliest
            earliest_key = min(self.cooldowns.keys(), key=lambda k: self.cooldowns[k])
            logger.warning(f"All API keys on cooldown. Waiting or returning earliest available key: ...{earliest_key[-4:]}")
            return earliest_key

    async def report_rate_limit(self, key: str, cooldown_seconds: float = 60.0):
        """Mark a key as rate limited for a specified cooldown duration."""
        async with self.lock:
            if key in self.cooldowns:
                self.cooldowns[key] = time.time() + cooldown_seconds
                logger.warning(f"API Key ...{key[-4:] if len(key)>4 else key} put on cooldown for {cooldown_seconds}s due to rate limit.")

    async def invoke_gemini(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        json_output: bool = False,
        fallback_json: Optional[Dict[str, Any]] = None,
        retries: int = 2
    ) -> Union[str, Dict[str, Any]]:
        """
        Invokes Gemini with automatic key rotation and retries.
        If no key is available or all fail, returns fallback_json or fallback string.
        """
        from google import genai
        from google.genai import types
        from google.genai.errors import APIError

        settings = get_settings()

        for attempt in range(retries + 1):
            key = await self.get_active_key()
            if not key:
                logger.info("No active Gemini API keys available. Using synthetic/fallback institutional reasoning.")
                return fallback_json if json_output else "Synthesized institutional reasoning via offline deterministic fallback."

            try:
                client = genai.Client(api_key=key)
                config_kwargs = {
                    "temperature": 0.2,
                }
                if system_instruction:
                    config_kwargs["system_instruction"] = system_instruction
                if json_output:
                    config_kwargs["response_mime_type"] = "application/json"

                config = types.GenerateContentConfig(**config_kwargs)

                # Run synchronously inside asyncio thread pool to avoid blocking
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: client.models.generate_content(
                        model=self.model_name,
                        contents=prompt,
                        config=config
                    )
                )

                if json_output:
                    try:
                        # Clean markdown codeblocks if present
                        text = response.text.strip()
                        if text.startswith("```json"):
                            text = text[7:]
                        if text.endswith("```"):
                            text = text[:-3]
                        return json.loads(text.strip())
                    except Exception as parse_err:
                        logger.warning(f"JSON parsing failed from Gemini output: {parse_err}. Returning fallback.")
                        return fallback_json or {}
                return response.text

            except APIError as api_err:
                err_str = str(api_err).lower()
                if "429" in err_str or "exhausted" in err_str or "quota" in err_str:
                    await self.report_rate_limit(key, cooldown_seconds=65.0)
                    logger.warning(f"Rate limit hit on attempt {attempt+1}/{retries+1}. Retrying with rotated key...")
                    await asyncio.sleep(1.0)
                    continue
                else:
                    logger.error(f"Gemini APIError: {api_err}")
                    break
            except Exception as e:
                logger.error(f"Unexpected error calling Gemini: {e}")
                await self.report_rate_limit(key, cooldown_seconds=30.0)
                await asyncio.sleep(0.5)

        logger.warning("All key retry attempts exhausted. Using institutional fallback synthesis.")
        return fallback_json if json_output else "Synthesized institutional reasoning via offline deterministic fallback."


# Global key manager instance
api_key_manager = APIKeyManager()
