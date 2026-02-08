"""
AI Service Layer for Medical Expert System.

Provides LLM integration via Groq API for conversational diagnosis assistance.
"""

from .llm_client import LLMClient, get_available_models
from .knowledge_base import KnowledgeBase
from .prompts import build_system_prompt, build_diagnosis_context

__all__ = [
    "LLMClient",
    "get_available_models", 
    "KnowledgeBase",
    "build_system_prompt",
    "build_diagnosis_context",
]
