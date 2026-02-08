"""
Prompt Engineering for Medical AI Assistant.

Builds system prompts that embed expert system rules as structured medical guidelines.
"""

from typing import Optional, List, Dict

# Core system prompt that establishes the AI's role and guidelines
SYSTEM_PROMPT_BASE = """You are a Medical Diagnostic Assistant powered by an expert system for tropical diseases. You help users understand their symptoms and provide guidance on possible conditions.

## Your Capabilities
- Analyze symptoms for: Cholera, Malaria, and Typhoid Fever
- Explain diagnostic criteria and reasoning
- Suggest when to seek medical care
- Reference WHO clinical guidelines

## Important Guidelines
1. **Never provide definitive diagnoses** - Only suggest possibilities and recommend professional evaluation
2. **Always recommend seeing a healthcare provider** for proper diagnosis and treatment
3. **Highlight danger signs** that require immediate medical attention
4. **Be empathetic** but clear in your communication
5. **Ask clarifying questions** when symptoms are vague
6. **Reference the expert system rules** when explaining diagnostic reasoning

## Danger Signs Requiring Immediate Care
- Altered consciousness or confusion
- Inability to drink or keep fluids down
- Severe dehydration (sunken eyes, skin pinch >2 seconds)
- High fever (>39.5°C) with rigors
- Bloody stool or vomit
- Convulsions or seizures
- Severe abdominal pain
- Dark/bloody urine (possible blackwater fever)

## Diagnostic Reasoning Framework
When analyzing symptoms, consider:
1. **Pathognomonic signs** (highly specific indicators)
2. **Symptom patterns** (cyclical fever, stepladder fever, etc.)
3. **Exposure history** (endemic area, unsafe water, travel)
4. **Symptom combinations** that increase diagnostic confidence
"""

# Expert system rules summary for AI reference
EXPERT_RULES_SUMMARY = """
## Expert System Diagnostic Rules

### CHOLERA
**Confident diagnosis:**
- Rice-water stool (pathognomonic) ± severe dehydration
- Acute watery diarrhea + vomiting + endemic exposure/unsafe water

**Key features:**
- Profuse watery diarrhea (can exceed 1L/hour in severe cases)
- Rapid dehydration
- NO fever typically
- Vomiting common

**Lab confirmation:** Stool culture for V. cholerae, Cholera RDT

### MALARIA
**Confident diagnosis:**
- Classic paroxysm: Cyclical fever + chills + sweating
- Fever + bitter taste in mouth + endemic exposure
- Any fever in traveler from endemic area within 30 days

**Key features:**
- Cyclical fever pattern (every 48-72 hours)
- Chills followed by high fever then sweating
- Bitter taste in mouth (highly suggestive)
- Headache, body aches, fatigue

**Severe malaria signs:**
- Cerebral: Altered consciousness, coma
- Respiratory distress
- Hemoglobinuria (dark/bloody urine - blackwater fever)
- Severe anemia (pale palms)

**Lab confirmation:** Blood smear for Plasmodium, Malaria RDT

### TYPHOID FEVER
**Confident diagnosis:**
- Stepladder fever + relative bradycardia (pathognomonic)
- Rose spots on trunk + fever + abdominal symptoms
- Prolonged fever (>7 days) + constipation + endemic exposure

**Key features:**
- Stepladder fever pattern (gradually increasing over days)
- Relative bradycardia (pulse slower than expected for fever)
- Rose spots (small pink macules on trunk)
- Constipation more common than diarrhea initially
- Abdominal discomfort, hepatosplenomegaly

**Danger signs:**
- Severe abdominal pain (possible perforation)
- Melena or bloody stool (intestinal bleeding)
- Altered consciousness (typhoid encephalopathy)

**Lab confirmation:** Blood culture for S. typhi, Widal test (titer ≥1:160), Typhidot

### DEHYDRATION ASSESSMENT (WHO)
**Severe (Plan C - IV fluids urgently):**
- Lethargic/unconscious + sunken eyes + skin pinch >2 seconds

**Some dehydration (Plan B - ORS):**
- Restless/irritable + drinks eagerly + slow skin pinch

**No dehydration (Plan A - home fluids):**
- Alert + drinks normally + normal skin pinch
"""

CONVERSATION_GUIDELINES = """
## Conversation Approach

1. **Start by understanding the chief complaint**
   - What brought you here today?
   - How long have you had these symptoms?

2. **Ask about key symptoms systematically**
   - Fever: pattern, duration, associated chills/sweating
   - GI symptoms: diarrhea (appearance), vomiting, pain
   - Other: headache, body aches, rash, urine changes

3. **Assess exposure risk**
   - Travel to endemic areas
   - Water and food safety
   - Contact with sick individuals

4. **Evaluate severity**
   - Can you drink fluids?
   - Any confusion or extreme weakness?
   - Any bloody symptoms?

5. **Provide assessment**
   - Explain which conditions are possible and why
   - Highlight concerning features
   - Recommend appropriate level of care
"""


def build_system_prompt(include_rules: bool = True, include_guidelines: bool = True) -> str:
    """
    Build the complete system prompt for the medical AI assistant.
    
    Args:
        include_rules: Include expert system diagnostic rules
        include_guidelines: Include conversation guidelines
        
    Returns:
        Complete system prompt string
    """
    parts = [SYSTEM_PROMPT_BASE]
    
    if include_rules:
        parts.append(EXPERT_RULES_SUMMARY)
    
    if include_guidelines:
        parts.append(CONVERSATION_GUIDELINES)
    
    return "\n".join(parts)


def build_diagnosis_context(
    symptoms: List[str] = None,
    patient_info: Dict = None,
    knowledge_context: List[Dict] = None,
) -> str:
    """
    Build additional context for a specific diagnosis query.
    
    Args:
        symptoms: List of reported symptoms
        patient_info: Patient demographics and exposure history
        knowledge_context: Retrieved knowledge chunks from RAG
        
    Returns:
        Context string to append to conversation
    """
    parts = []
    
    if patient_info:
        parts.append("## Patient Context")
        context_items = []
        if patient_info.get("age"):
            context_items.append(f"- Age: {patient_info['age']} years")
        if patient_info.get("is_pregnant"):
            context_items.append("- Pregnant: Yes")
        if patient_info.get("travel_endemic_area"):
            context_items.append("- Recent travel to endemic area: Yes")
        if patient_info.get("endemic_resident"):
            context_items.append("- Lives in endemic area: Yes")
        if patient_info.get("unsafe_water"):
            context_items.append("- Consumed untreated water: Yes")
        if patient_info.get("household_contact"):
            context_items.append("- Contact with confirmed case: Yes")
        if context_items:
            parts.append("\n".join(context_items))
    
    if symptoms:
        parts.append("\n## Reported Symptoms")
        for symptom in symptoms:
            parts.append(f"- {symptom.replace('_', ' ').title()}")
    
    if knowledge_context:
        parts.append("\n## Relevant Medical Knowledge")
        for chunk in knowledge_context[:3]:  # Limit to top 3
            parts.append(f"\n### {chunk.get('title', 'Reference')} ({chunk.get('disease', 'General')})")
            content = chunk.get('content', '')
            # Truncate long content
            if len(content) > 800:
                content = content[:800] + "..."
            parts.append(content)
    
    return "\n".join(parts) if parts else ""


def build_user_message_with_context(
    user_message: str,
    context: Optional[str] = None,
) -> str:
    """
    Build user message with optional context prepended.
    
    Args:
        user_message: The user's actual message
        context: Additional context to include
        
    Returns:
        Formatted user message
    """
    if context:
        return f"{context}\n\n---\n\nUser message: {user_message}"
    return user_message
