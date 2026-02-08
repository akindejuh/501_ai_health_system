"""
Expert System API Router.

Provides structured endpoints for direct interaction with the medical diagnosis expert system.
"""

from ninja import Router
from typing import Optional, List

from src.lib.expert_system.diagnosis_engine import run_diagnosis
from src.api.schemas.expert import (
    DiagnoseRequest,
    DiagnoseResponse,
    DiagnosisResult,
    SymptomInfo,
    DiseaseInfo,
)


router = Router(tags=["Expert System"])


# Valid symptoms the expert system accepts
VALID_SYMPTOMS = {
    "fever": {
        "display_name": "Fever",
        "description": "Elevated body temperature",
        "options": {
            "pattern": ["cyclical", "stepladder", "continuous", "irregular"],
            "severity": ["mild", "moderate", "severe"],
        }
    },
    "chills": {
        "display_name": "Chills/Rigors",
        "description": "Shaking or shivering episodes",
        "options": None,
    },
    "sweating": {
        "display_name": "Profuse Sweating",
        "description": "Heavy sweating episodes, often after fever",
        "options": None,
    },
    "diarrhea": {
        "display_name": "Diarrhea",
        "description": "Loose or watery stools",
        "options": {
            "description": ["rice_water", "watery", "bloody", "mucoid"],
            "severity": ["mild", "moderate", "severe"],
        }
    },
    "vomiting": {
        "display_name": "Vomiting",
        "description": "Nausea and vomiting",
        "options": {
            "severity": ["mild", "moderate", "severe"],
        }
    },
    "dehydration": {
        "display_name": "Dehydration",
        "description": "Signs of fluid loss",
        "options": {
            "severity": ["mild", "moderate", "severe"],
        }
    },
    "headache": {
        "display_name": "Headache",
        "description": "Head pain",
        "options": {
            "severity": ["mild", "moderate", "severe"],
        }
    },
    "abdominal_pain": {
        "display_name": "Abdominal Pain",
        "description": "Stomach or belly pain",
        "options": {
            "severity": ["mild", "moderate", "severe"],
        }
    },
    "severe_abdominal_pain": {
        "display_name": "Severe Abdominal Pain",
        "description": "Intense abdominal pain (danger sign)",
        "options": None,
    },
    "constipation": {
        "display_name": "Constipation",
        "description": "Difficulty passing stool",
        "options": None,
    },
    "bitter_taste": {
        "display_name": "Bitter Taste",
        "description": "Bitter taste in mouth (suggestive of malaria)",
        "options": None,
    },
    "rose_spots": {
        "display_name": "Rose Spots",
        "description": "Small pink macules on trunk (suggestive of typhoid)",
        "options": None,
    },
    "relative_bradycardia": {
        "display_name": "Relative Bradycardia",
        "description": "Pulse slower than expected for fever level",
        "options": None,
    },
    "altered_consciousness": {
        "display_name": "Altered Consciousness",
        "description": "Confusion, drowsiness, or disorientation",
        "options": None,
    },
    "convulsions": {
        "display_name": "Convulsions/Seizures",
        "description": "Seizure activity",
        "options": None,
    },
    "body_aches": {
        "display_name": "Body Aches",
        "description": "Muscle and joint pain",
        "options": None,
    },
    "dark_urine": {
        "display_name": "Dark/Bloody Urine",
        "description": "Abnormal urine color",
        "options": {
            "description": ["dark", "brown", "cola", "red", "bloody", "black"],
        }
    },
    "anemia": {
        "display_name": "Anemia/Pallor",
        "description": "Pale palms or conjunctiva",
        "options": {
            "severity": ["mild", "moderate", "severe"],
        }
    },
    "melena": {
        "display_name": "Melena",
        "description": "Black tarry stools (intestinal bleeding)",
        "options": None,
    },
    "bloody_stool": {
        "display_name": "Bloody Stool",
        "description": "Visible blood in stool",
        "options": None,
    },
}


# Disease information
DISEASES = {
    "cholera": {
        "name": "Cholera",
        "description": "Acute diarrheal infection caused by Vibrio cholerae bacteria, spread through contaminated water",
        "key_symptoms": ["diarrhea", "vomiting", "dehydration"],
        "pathognomonic_signs": ["Rice-water stool (pale, milky with mucus flecks)"],
    },
    "malaria": {
        "name": "Malaria",
        "description": "Parasitic disease transmitted by infected Anopheles mosquitoes, caused by Plasmodium parasites",
        "key_symptoms": ["fever", "chills", "sweating", "headache", "body_aches"],
        "pathognomonic_signs": [
            "Classic malarial paroxysm (cyclical fever + chills + sweating)",
            "Bitter taste in mouth",
        ],
    },
    "typhoid_fever": {
        "name": "Typhoid Fever",
        "description": "Enteric fever caused by Salmonella typhi bacteria, spread through contaminated food/water",
        "key_symptoms": ["fever", "headache", "abdominal_pain", "constipation"],
        "pathognomonic_signs": [
            "Stepladder fever pattern (gradually increasing)",
            "Relative bradycardia",
            "Rose spots on trunk",
        ],
    },
}


@router.post(
    "/diagnose",
    response=DiagnoseResponse,
    summary="Run expert system diagnosis",
    description="Analyze symptoms using the rule-based expert system and return possible diagnoses.",
)
def diagnose(request, data: DiagnoseRequest):
    """
    Run diagnosis using the medical expert system.
    
    The expert system uses rule-based reasoning to evaluate symptoms and
    return possible diagnoses with confidence levels.
    """
    # Convert Pydantic models to dicts for the expert system
    symptoms = [s.model_dump(exclude_none=True) for s in data.symptoms]
    patient_info = data.patient.model_dump(exclude_none=True) if data.patient else None
    lab_results = [l.model_dump(exclude_none=True) for l in data.lab_results] if data.lab_results else None
    dehydration_signs = [d.model_dump(exclude_none=True) for d in data.dehydration_signs] if data.dehydration_signs else None
    
    # Run the expert system
    result = run_diagnosis(
        symptoms=symptoms,
        patient_info=patient_info,
        lab_results=lab_results,
        dehydration_signs=dehydration_signs,
    )
    
    # Transform diagnoses to response format
    diagnoses = []
    for diag in result.get("diagnoses", []):
        diagnoses.append(DiagnosisResult(
            disease=diag.get("disease", "unknown"),
            confidence=diag.get("confidence", "uncertain"),
            reason=diag.get("reason", ""),
            severity=diag.get("severity"),
            recommendation=diag.get("recommendation"),
        ))
    
    # Sort by confidence level
    confidence_order = {"confirmed": 0, "confident": 1, "suspect": 2, "uncertain": 3}
    diagnoses.sort(key=lambda d: confidence_order.get(d.confidence, 4))
    
    # Extract dehydration info if present
    dehydration_level = None
    treatment_plan = None
    for rec in result.get("recommendations", []):
        if "dehydration" in rec.lower():
            # Parse dehydration info from recommendations
            if "severe" in rec.lower():
                dehydration_level = "severe"
                treatment_plan = "C"
            elif "some" in rec.lower() or "moderate" in rec.lower():
                dehydration_level = "some"
                treatment_plan = "B"
            elif "no dehydration" in rec.lower() or "none" in rec.lower():
                dehydration_level = "none"
                treatment_plan = "A"
    
    return DiagnoseResponse(
        diagnoses=diagnoses,
        recommendations=result.get("recommendations", []),
        dehydration_level=dehydration_level,
        treatment_plan=treatment_plan,
    )


@router.get(
    "/symptoms",
    response=List[SymptomInfo],
    summary="List valid symptoms",
    description="Get list of all symptoms the expert system recognizes with their options.",
)
def list_symptoms(request):
    """Return all valid symptoms the expert system accepts."""
    return [
        SymptomInfo(
            name=name,
            display_name=info["display_name"],
            description=info["description"],
            options=info["options"],
        )
        for name, info in VALID_SYMPTOMS.items()
    ]


@router.get(
    "/diseases",
    response=List[DiseaseInfo],
    summary="List supported diseases",
    description="Get list of diseases the expert system can diagnose.",
)
def list_diseases(request):
    """Return all diseases the expert system can diagnose."""
    return [
        DiseaseInfo(
            name=info["name"],
            description=info["description"],
            key_symptoms=info["key_symptoms"],
            pathognomonic_signs=info["pathognomonic_signs"],
        )
        for info in DISEASES.values()
    ]


@router.get(
    "/diseases/{disease_name}",
    response=DiseaseInfo,
    summary="Get disease info",
    description="Get detailed information about a specific disease.",
)
def get_disease(request, disease_name: str):
    """Get information about a specific disease."""
    disease_key = disease_name.lower().replace(" ", "_").replace("-", "_")
    
    if disease_key not in DISEASES:
        from ninja.errors import HttpError
        raise HttpError(404, f"Disease '{disease_name}' not found. Available: {list(DISEASES.keys())}")
    
    info = DISEASES[disease_key]
    return DiseaseInfo(
        name=info["name"],
        description=info["description"],
        key_symptoms=info["key_symptoms"],
        pathognomonic_signs=info["pathognomonic_signs"],
    )
