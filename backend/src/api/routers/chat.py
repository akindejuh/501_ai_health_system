"""
AI Chat API Router.

Provides conversational interface powered by LLM with expert system knowledge as context.
"""

import asyncio
import re
from ninja import Router
from typing import Optional, List

from src.lib.ai.llm_client import LLMClient, get_available_models, DEFAULT_MODEL
from src.lib.ai.knowledge_base import get_knowledge_base
from src.lib.ai.prompts import build_system_prompt, build_diagnosis_context
from src.api.schemas.chat import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ModelInfo,
    ModelSettingsRequest,
    ModelsResponse,
)


router = Router(tags=["AI Chat"])


# Symptom keywords for extraction
SYMPTOM_KEYWORDS = {
    "fever": ["fever", "febrile", "temperature", "hot"],
    "chills": ["chills", "rigors", "shivering", "shaking"],
    "sweating": ["sweating", "sweats", "diaphoresis", "perspiration"],
    "diarrhea": ["diarrhea", "diarrhoea", "loose stool", "watery stool"],
    "vomiting": ["vomiting", "vomit", "throwing up", "nausea"],
    "headache": ["headache", "head pain", "head ache"],
    "abdominal_pain": ["abdominal pain", "stomach pain", "belly pain", "tummy pain"],
    "body_aches": ["body aches", "muscle pain", "joint pain", "myalgia", "arthralgia"],
    "bitter_taste": ["bitter taste", "bitter mouth"],
    "constipation": ["constipation", "constipated"],
    "dehydration": ["dehydrated", "dehydration", "thirsty", "dry mouth"],
    "dark_urine": ["dark urine", "brown urine", "bloody urine", "cola urine"],
    "weakness": ["weakness", "weak", "fatigue", "tired", "exhausted"],
    "confusion": ["confusion", "confused", "disoriented", "altered consciousness"],
}

# Disease keywords for context retrieval
DISEASE_KEYWORDS = {
    "malaria": ["malaria", "mosquito", "plasmodium"],
    "cholera": ["cholera", "vibrio", "rice water"],
    "typhoid": ["typhoid", "typhoid fever", "salmonella", "enteric fever"],
}


def extract_symptoms_from_text(text: str) -> List[str]:
    """Extract mentioned symptoms from user text."""
    text_lower = text.lower()
    found_symptoms = []
    
    for symptom, keywords in SYMPTOM_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_symptoms.append(symptom)
                break
    
    return list(set(found_symptoms))


def extract_diseases_from_text(text: str) -> List[str]:
    """Extract mentioned diseases from user text."""
    text_lower = text.lower()
    found_diseases = []
    
    for disease, keywords in DISEASE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_diseases.append(disease)
                break
    
    return list(set(found_diseases))


def run_async(coro):
    """Run async coroutine in sync context."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Create a new loop if current is running
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)


@router.post(
    "/message",
    response=ChatResponse,
    summary="Send chat message",
    description="Send a message to the AI assistant and receive a response with medical guidance.",
)
def chat_message(request, data: ChatRequest):
    """
    Chat with the medical AI assistant.
    
    The assistant uses LLM capabilities enhanced with expert system knowledge
    to provide helpful medical guidance.
    """
    # Extract symptoms and diseases from conversation for context
    all_text = data.message
    for msg in data.conversation_history:
        all_text += " " + msg.content
    
    extracted_symptoms = extract_symptoms_from_text(all_text)
    extracted_diseases = extract_diseases_from_text(all_text)
    
    # Get relevant knowledge context if enabled
    knowledge_context = []
    if data.include_expert_context and (extracted_symptoms or extracted_diseases):
        kb = get_knowledge_base()
        knowledge_context = kb.get_relevant_context(
            symptoms=extracted_symptoms,
            diseases=extracted_diseases if extracted_diseases else None,
            query=data.message,
            max_chunks=3,
        )
    
    # Build messages for LLM
    messages = []
    
    # System prompt with expert rules
    system_prompt = build_system_prompt(
        include_rules=data.include_expert_context,
        include_guidelines=True,
    )
    messages.append({"role": "system", "content": system_prompt})
    
    # Add conversation history
    for msg in data.conversation_history:
        messages.append({"role": msg.role, "content": msg.content})
    
    # Build user message with context
    user_message = data.message
    if knowledge_context or data.patient_context:
        context = build_diagnosis_context(
            symptoms=extracted_symptoms if extracted_symptoms else None,
            patient_info=data.patient_context,
            knowledge_context=knowledge_context,
        )
        if context:
            user_message = f"[Context for assistant - user provided symptoms: {', '.join(extracted_symptoms) if extracted_symptoms else 'none extracted yet'}]\n\n{context}\n\n---\n\nUser: {data.message}"
    
    messages.append({"role": "user", "content": user_message})
    
    # Call LLM
    model = data.model or DEFAULT_MODEL
    client = LLMClient(model=model)
    
    try:
        response_text = run_async(client.chat(
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        ))
    except Exception as e:
        response_text = f"I apologize, but I encountered an error processing your request. Please try again or rephrase your question. (Error: {str(e)})"
    
    # Update conversation history
    updated_history = list(data.conversation_history)
    updated_history.append(ChatMessage(role="user", content=data.message))
    updated_history.append(ChatMessage(role="assistant", content=response_text))
    
    # Extract any new symptoms mentioned in the response
    suggested_diseases = None
    if extracted_symptoms:
        # Based on extracted symptoms, suggest relevant diseases
        suggested = []
        if any(s in ["fever", "chills", "sweating", "bitter_taste"] for s in extracted_symptoms):
            suggested.append("malaria")
        if any(s in ["diarrhea", "vomiting", "dehydration"] for s in extracted_symptoms):
            suggested.append("cholera")
        if any(s in ["fever", "constipation", "abdominal_pain"] for s in extracted_symptoms):
            suggested.append("typhoid_fever")
        if suggested:
            suggested_diseases = list(set(suggested))
    
    return ChatResponse(
        response=response_text,
        model_used=model,
        conversation_history=updated_history,
        extracted_symptoms=extracted_symptoms if extracted_symptoms else None,
        suggested_diseases=suggested_diseases,
    )


@router.get(
    "/models",
    response=ModelsResponse,
    summary="List available models",
    description="Get list of available LLM models that can be used for chat.",
)
def list_models(request):
    """Return all available LLM models."""
    models = [
        ModelInfo(**m) for m in get_available_models()
    ]
    return ModelsResponse(
        models=models,
        default_model=DEFAULT_MODEL,
        current_model=None,  # Stateless - no session tracking
    )


@router.post(
    "/validate-model",
    summary="Validate model selection",
    description="Check if a model ID is valid.",
)
def validate_model(request, data: ModelSettingsRequest):
    """Validate that a model ID is available."""
    available = [m["id"] for m in get_available_models()]
    is_valid = data.model in available
    
    return {
        "model": data.model,
        "valid": is_valid,
        "available_models": available if not is_valid else None,
    }
