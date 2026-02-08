"""
Pydantic schemas for Expert System API endpoints.
"""

from typing import Optional, Literal, List, Dict
from pydantic import BaseModel, Field


class SymptomInput(BaseModel):
    """Input schema for a single symptom."""
    name: str = Field(..., description="Symptom name (e.g., 'fever', 'diarrhea')")
    present: bool = Field(True, description="Whether the symptom is present")
    severity: Optional[Literal["mild", "moderate", "severe"]] = Field(
        None, description="Symptom severity"
    )
    duration_days: Optional[int] = Field(None, description="Duration in days", ge=0)
    pattern: Optional[str] = Field(
        None, description="Pattern (e.g., 'cyclical', 'stepladder', 'continuous')"
    )
    description: Optional[str] = Field(
        None, description="Additional details (e.g., 'rice_water', 'watery', 'bloody')"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "fever", "present": True, "pattern": "cyclical"},
                {"name": "diarrhea", "present": True, "severity": "severe", "description": "rice_water"},
            ]
        }
    }


class PatientInput(BaseModel):
    """Input schema for patient information."""
    age: Optional[int] = Field(None, description="Patient age in years", ge=0, le=150)
    is_child: Optional[bool] = Field(None, description="Is patient under 18")
    is_pregnant: Optional[bool] = Field(None, description="Is patient pregnant")
    travel_endemic_area: Optional[bool] = Field(
        None, description="Recent travel to endemic area (within 30 days)"
    )
    endemic_resident: Optional[bool] = Field(
        None, description="Lives in endemic area"
    )
    unsafe_water: Optional[bool] = Field(
        None, description="Consumed unboiled/untreated water"
    )
    street_food: Optional[bool] = Field(
        None, description="Consumed raw street food"
    )
    household_contact: Optional[bool] = Field(
        None, description="Contact with confirmed cholera/typhoid/malaria case"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "age": 35,
                    "travel_endemic_area": True,
                    "unsafe_water": True,
                }
            ]
        }
    }


class LabResultInput(BaseModel):
    """Input schema for laboratory test results."""
    test: str = Field(
        ..., 
        description="Test name (blood_smear, rdt_malaria, stool_culture, rdt_cholera, blood_culture, widal, typhidot)"
    )
    result: Literal["positive", "negative", "pending"] = Field(
        ..., description="Test result"
    )
    details: Optional[str] = Field(
        None, description="Additional details (e.g., species, titer like '1:320')"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"test": "blood_smear", "result": "positive", "details": "P. falciparum"},
                {"test": "widal", "result": "positive", "details": "1:320"},
            ]
        }
    }


class DehydrationSignInput(BaseModel):
    """Input schema for dehydration assessment signs."""
    sign: Literal["mental_state", "eyes", "skin_pinch", "thirst"] = Field(
        ..., description="Sign being assessed"
    )
    finding: str = Field(
        ..., 
        description="Observed finding (mental_state: alert/restless/lethargic/unconscious; "
                    "eyes: normal/sunken; skin_pinch: normal/slow/very_slow; "
                    "thirst: drinks_normally/drinks_eagerly/unable_to_drink)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"sign": "mental_state", "finding": "restless"},
                {"sign": "skin_pinch", "finding": "slow"},
            ]
        }
    }


class DiagnoseRequest(BaseModel):
    """Request schema for diagnosis endpoint."""
    symptoms: List[SymptomInput] = Field(
        ..., description="List of symptoms to analyze", min_length=1
    )
    patient: Optional[PatientInput] = Field(
        None, description="Patient demographics and exposure history"
    )
    lab_results: Optional[List[LabResultInput]] = Field(
        None, description="Laboratory test results if available"
    )
    dehydration_signs: Optional[List[DehydrationSignInput]] = Field(
        None, description="WHO dehydration assessment signs"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "symptoms": [
                        {"name": "fever", "present": True, "pattern": "cyclical"},
                        {"name": "chills", "present": True},
                        {"name": "sweating", "present": True},
                    ],
                    "patient": {
                        "age": 28,
                        "travel_endemic_area": True,
                    }
                }
            ]
        }
    }


class DiagnosisResult(BaseModel):
    """A single diagnosis result from the expert system."""
    disease: str = Field(..., description="Disease name")
    confidence: Literal["confirmed", "confident", "suspect", "uncertain"] = Field(
        ..., description="Confidence level"
    )
    reason: str = Field(..., description="Reasoning for this diagnosis")
    severity: Optional[str] = Field(None, description="Severity if applicable")
    recommendation: Optional[str] = Field(None, description="Recommended next steps")


class DiagnoseResponse(BaseModel):
    """Response schema for diagnosis endpoint."""
    diagnoses: List[DiagnosisResult] = Field(
        ..., description="List of possible diagnoses ranked by confidence"
    )
    recommendations: List[str] = Field(
        default_factory=list, description="General recommendations and urgent actions"
    )
    dehydration_level: Optional[str] = Field(
        None, description="WHO dehydration classification if assessed"
    )
    treatment_plan: Optional[str] = Field(
        None, description="WHO treatment plan (A/B/C) if dehydration assessed"
    )
    disclaimer: str = Field(
        default="This is an expert system assessment, not a medical diagnosis. "
                "Please consult a healthcare professional for proper evaluation and treatment.",
        description="Medical disclaimer"
    )


class SymptomInfo(BaseModel):
    """Information about a valid symptom for the expert system."""
    name: str = Field(..., description="Symptom identifier")
    display_name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="Description of the symptom")
    options: Optional[Dict] = Field(None, description="Available options/values")


class DiseaseInfo(BaseModel):
    """Information about a disease the system can diagnose."""
    name: str = Field(..., description="Disease name")
    description: str = Field(..., description="Brief description")
    key_symptoms: List[str] = Field(..., description="Key symptoms to look for")
    pathognomonic_signs: List[str] = Field(
        default_factory=list, description="Highly specific signs for this disease"
    )
