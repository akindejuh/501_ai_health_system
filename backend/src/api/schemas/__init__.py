"""
API Schemas Package.

Pydantic models for request/response validation.
"""

from .expert import (
    SymptomInput,
    PatientInput,
    LabResultInput,
    DehydrationSignInput,
    DiagnoseRequest,
    DiagnosisResult,
    DiagnoseResponse,
    SymptomInfo,
    DiseaseInfo,
)

from .chat import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ModelInfo,
    ModelSettingsRequest,
)

__all__ = [
    # Expert schemas
    "SymptomInput",
    "PatientInput", 
    "LabResultInput",
    "DehydrationSignInput",
    "DiagnoseRequest",
    "DiagnosisResult",
    "DiagnoseResponse",
    "SymptomInfo",
    "DiseaseInfo",
    # Chat schemas
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "ModelInfo",
    "ModelSettingsRequest",
]
