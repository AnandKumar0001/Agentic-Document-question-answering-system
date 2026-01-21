"""LLM interface for local Ollama models."""
import requests
from typing import List, Dict, Any

try:
    from .config import LLM_BASE_URL, LLM_MODEL
except ImportError:
    from config import LLM_BASE_URL, LLM_MODEL


class LocalLLM:
    """Interface for local LLM using Ollama."""

    def __init__(self, model: str = LLM_MODEL, base_url: str = LLM_BASE_URL):
        """Initialize local LLM handler."""
        self.model = model
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/generate"

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 512) -> str:
        """Generate text using local LLM."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "num_predict": max_tokens,
                "stream": False
            }

            response = requests.post(self.api_endpoint, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""

    def generate_streaming(self, prompt: str, temperature: float = 0.7):
        """Generate text with streaming."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": True
            }

            response = requests.post(self.api_endpoint, json=payload, stream=True, timeout=30)
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    chunk = line.decode('utf-8')
                    yield chunk
        except Exception as e:
            print(f"Error in streaming: {e}")

    def is_available(self) -> bool:
        """Check if LLM is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
