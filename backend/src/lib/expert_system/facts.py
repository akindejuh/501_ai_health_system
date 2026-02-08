"""
Fact definitions for the Medical Diagnostic Expert System.

This module defines the knowledge representation structures used by the
diagnosis engine to reason about patient symptoms and arrive at diagnoses.
"""

from experta import Fact


class Patient(Fact):
    """
    Patient demographics and history.
    
    Fields:
        age: int - Patient age in years
        is_child: bool - True if age < 18
        is_pregnant: bool - Pregnancy status (relevant for treatment)
        travel_endemic_area: bool - Recent travel to endemic region
        endemic_resident: bool - Lives in endemic area
        blood_group: str - Blood group (O has higher risk for some diseases)
        household_contact: bool - Contact with confirmed case
        unsafe_water: bool - Consumed unboiled/untreated water
        street_food: bool - Consumed raw street food
    """
    pass


class Symptom(Fact):
    """
    Individual symptom observation.
    
    Fields:
        name: str - Symptom identifier (e.g., 'fever', 'diarrhea', 'vomiting')
        present: bool - Whether symptom is present
        severity: str - 'mild', 'moderate', 'severe' (optional)
        duration_days: int - How long symptom has been present (optional)
        pattern: str - Specific pattern (e.g., 'cyclical', 'stepladder') (optional)
        description: str - Additional details (e.g., 'rice-water' for stool)
    """
    pass


class VitalSign(Fact):
    """
    Vital sign measurement.
    
    Fields:
        type: str - 'temperature', 'heart_rate', 'respiratory_rate', 'blood_pressure'
        value: float - Measured value
        unit: str - Unit of measurement
        interpretation: str - 'normal', 'low', 'high', 'critical' (optional)
    """
    pass


class DehydrationSign(Fact):
    """
    Dehydration assessment sign (WHO classification).
    
    Fields:
        sign: str - Sign name (e.g., 'skin_pinch', 'eyes', 'mental_state', 'thirst')
        finding: str - Observed finding
    """
    pass


class LabResult(Fact):
    """
    Laboratory test result.
    
    Fields:
        test: str - Test name (e.g., 'blood_smear', 'rdt_malaria', 'stool_culture', 'widal')
        result: str - Test outcome ('positive', 'negative', 'pending')
        details: str - Additional details (e.g., species, titer)
    """
    pass


class DehydrationLevel(Fact):
    """
    WHO Dehydration classification result.
    
    Fields:
        level: str - 'none', 'some', 'severe'
        treatment_plan: str - 'A', 'B', 'C'
    """
    pass


class SeverityIndicator(Fact):
    """
    Indicator of severe/complicated disease.
    
    Fields:
        indicator: str - Name of danger sign
        disease: str - Associated disease (optional)
        action: str - Required action (e.g., 'urgent_referral')
    """
    pass


class Diagnosis(Fact):
    """
    Diagnosis conclusion from the expert system.
    
    Fields:
        disease: str - Disease name ('cholera', 'malaria', 'typhoid', 'uncertain')
        confidence: str - 'confident', 'suspect', 'uncertain'
        reason: str - Key finding(s) that led to this diagnosis
        severity: str - 'uncomplicated', 'severe' (optional)
        recommendation: str - Next steps (optional)
    """
    pass


class TreatmentPlan(Fact):
    """
    Treatment recommendation.
    
    Fields:
        disease: str - Target disease
        plan_type: str - e.g., 'rehydration', 'antibiotic', 'antimalarial'
        medication: str - Drug name
        dosage: str - Dosage instructions
        duration: str - Treatment duration
        notes: str - Special considerations
    """
    pass
