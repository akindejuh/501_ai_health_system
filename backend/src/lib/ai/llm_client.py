"""
LLM Client for Groq API.

Provides async interface to Groq's OpenAI-compatible API with model switching support.
"""

import os
import httpx
from typing import AsyncGenerator, Optional, List, Dict, Union
from dataclasses import dataclass


@dataclass
class ModelInfo:
    """Information about an available LLM model."""
    id: str
    name: str
    description: str
    context_window: int
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "context_window": self.context_window,
        }


# Available models on Groq (free tier)
AVAILABLE_MODELS = {
    "llama-3.3-70b-versatile": ModelInfo(
        id="llama-3.3-70b-versatile",
        name="Llama 3.3 70B",
        description="Meta's latest Llama model, excellent for medical reasoning",
        context_window=128000,
    ),
    "llama-3.1-8b-instant": ModelInfo(
        id="llama-3.1-8b-instant",
        name="Llama 3.1 8B Instant",
        description="Fast, smaller Llama model for quick responses",
        context_window=128000,
    ),
    "mixtral-8x7b-32768": ModelInfo(
        id="mixtral-8x7b-32768",
        name="Mixtral 8x7B",
        description="Mistral's mixture-of-experts model",
        context_window=32768,
    ),
    "gemma2-9b-it": ModelInfo(
        id="gemma2-9b-it",
        name="Gemma 2 9B",
        description="Google's efficient instruction-tuned model",
        context_window=8192,
    ),
}

DEFAULT_MODEL = "llama-3.3-70b-versatile"


def get_available_models() -> List[Dict]:
    """Return list of available models with their info."""
    return [model.to_dict() for model in AVAILABLE_MODELS.values()]


class LLMClient:
    """
    Async client for Groq's OpenAI-compatible API.
    
    Usage:
        client = LLMClient()
        response = await client.chat([
            {"role": "system", "content": "You are a medical assistant."},
            {"role": "user", "content": "I have a fever and chills."}
        ])
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = DEFAULT_MODEL,
    ):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.base_url = (base_url or os.getenv("OPEN_API_BASE_URL", "https://api.groq.com/openai/v1")).rstrip("/")
        self.model = model
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set. Please set it in environment or .env file.")
    
    def set_model(self, model_id: str) -> None:
        """Switch to a different model."""
        if model_id not in AVAILABLE_MODELS:
            raise ValueError(f"Unknown model: {model_id}. Available: {list(AVAILABLE_MODELS.keys())}")
        self.model = model_id
    
    def get_current_model(self) -> dict:
        """Get info about the currently selected model."""
        return AVAILABLE_MODELS[self.model].to_dict()
    
    async def chat(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False,
    ) -> Union[str, AsyncGenerator[str, None]]:
        """
        Send a chat completion request.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            stream: If True, returns an async generator for streaming
            
        Returns:
            Response text or async generator if streaming
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }
        
        if stream:
            return self._stream_response(headers, payload)
        else:
            return await self._get_response(headers, payload)
    
    async def _get_response(self, headers: dict, payload: dict) -> str:
        """Get non-streaming response."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    async def _stream_response(self, headers: dict, payload: dict) -> AsyncGenerator[str, None]:
        """Stream response chunks."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            import json
                            chunk = json.loads(data)
                            delta = chunk["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                        except (json.JSONDecodeError, KeyError):
                            continue
