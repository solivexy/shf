"""
Groq LLM Wrapper for DeepEval Evaluation Framework.
Uses OpenAI-compatible Groq API to power G-Eval metrics as the LLM judge.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
from deepeval.models import DeepEvalBaseLLM

# Load environment from the project root .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


class GroqEvalLLM(DeepEvalBaseLLM):
    """
    Custom DeepEval LLM wrapper that routes evaluation prompts
    through the Groq API using their OpenAI-compatible endpoint.
    """

    def __init__(self, model_name: str = "openai/gpt-oss-120b"):
        self.model_name = model_name
        self._client = OpenAI(
            api_key=os.environ.get("GROQ_API_KEY", ""),
            base_url="https://api.groq.com/openai/v1",
        )

    def load_model(self):
        return self.model_name

    def generate(self, prompt: str, schema=None) -> str:
        """Synchronous generation via Groq API."""
        try:
            response = self._client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=4096,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[GroqEvalLLM Error] {e}"

    async def a_generate(self, prompt: str, schema=None) -> str:
        """Async generation (delegates to sync for simplicity)."""
        return self.generate(prompt, schema)

    def get_model_name(self) -> str:
        return self.model_name
