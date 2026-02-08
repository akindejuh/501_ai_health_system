"""
Pydantic schemas for AI Chat API endpoints.
"""

from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single message in the conversation."""
    role: Literal["user", "assistant", "system"] = Field(
        ..., description="Message role"
    )
    content: str = Field(..., description="Message content")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"role": "user", "content": "I have had fever and chills for 3 days"},
                {"role": "assistant", "content": "I'm sorry to hear you're not feeling well..."},
            ]
        }
    }


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(..., description="User's message", min_length=1)
    conversation_history: List[ChatMessage] = Field(
        default_factory=list,
        description="Previous messages in the conversation for context"
    )
    model: Optional[str] = Field(
        None, description="Model to use (defaults to llama-3.3-70b-versatile)"
    )
    include_expert_context: bool = Field(
        True, description="Whether to include expert system context in AI reasoning"
    )
    patient_context: Optional[dict] = Field(
        None, description="Optional patient info for more relevant responses"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "I've been having fever and chills for the past 3 days. I recently traveled to Nigeria.",
                    "conversation_history": [],
                    "include_expert_context": True,
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    response: str = Field(..., description="AI assistant's response")
    model_used: str = Field(..., description="Model that generated the response")
    conversation_history: List[ChatMessage] = Field(
        ..., description="Updated conversation history including this exchange"
    )
    extracted_symptoms: Optional[List[str]] = Field(
        None, description="Symptoms extracted from the conversation (if any)"
    )
    suggested_diseases: Optional[List[str]] = Field(
        None, description="Diseases suggested based on conversation"
    )


class ModelInfo(BaseModel):
    """Information about an available LLM model."""
    id: str = Field(..., description="Model identifier")
    name: str = Field(..., description="Display name")
    description: str = Field(..., description="Model description")
    context_window: int = Field(..., description="Maximum context window size")


class ModelSettingsRequest(BaseModel):
    """Request to change model settings."""
    model: str = Field(..., description="Model ID to switch to")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"model": "llama-3.3-70b-versatile"},
                {"model": "mixtral-8x7b-32768"},
            ]
        }
    }


class ModelsResponse(BaseModel):
    """Response listing available models."""
    models: List[ModelInfo] = Field(..., description="List of available models")
    default_model: str = Field(..., description="Default model ID")
    current_model: Optional[str] = Field(None, description="Currently selected model")
