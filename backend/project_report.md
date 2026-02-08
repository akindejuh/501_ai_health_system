# Project Report: Medical Expert System API

**Document Version:** 1.0  
**Last Updated:** February 8, 2026  
**Project Status:** Phase 1 Complete (MVP)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Goals & Objectives](#2-project-goals--objectives)
3. [System Architecture](#3-system-architecture)
4. [Technology Stack & Rationale](#4-technology-stack--rationale)
5. [Expert System Design](#5-expert-system-design)
6. [AI Integration Layer](#6-ai-integration-layer)
7. [API Design & Endpoints](#7-api-design--endpoints)
8. [Data Flow & Sequence Diagrams](#8-data-flow--sequence-diagrams)
9. [Knowledge Base Structure](#9-knowledge-base-structure)
10. [Security Considerations](#10-security-considerations)
11. [Performance Considerations](#11-performance-considerations)
12. [Testing Strategy](#12-testing-strategy)
13. [Deployment Architecture](#13-deployment-architecture)
14. [Future Roadmap](#14-future-roadmap)
15. [Known Limitations](#15-known-limitations)
16. [Appendices](#16-appendices)

---

## 1. Executive Summary

### 1.1 Project Overview

The Medical Expert System API is a hybrid diagnostic assistance platform that combines **rule-based expert system reasoning** with **Large Language Model (LLM) capabilities** to provide medical diagnostic guidance for tropical diseases.

### 1.2 Problem Statement

Healthcare workers in endemic regions often face:
- Limited access to specialist consultations
- High patient volumes requiring rapid triage
- Need for consistent application of WHO clinical guidelines
- Language barriers in patient communication

### 1.3 Solution

A dual-mode API system that provides:
1. **Structured Expert System** — Deterministic, rule-based diagnosis following WHO protocols
2. **AI Chat Assistant** — Natural language interface powered by LLMs with expert knowledge as context

### 1.4 Current Scope

| Disease | Status | Confidence |
|---------|--------|------------|
| Cholera | ✅ Implemented | High |
| Malaria | ✅ Implemented | High |
| Typhoid Fever | ✅ Implemented | High |

### 1.5 Key Metrics

- **Rules Implemented:** 50+ diagnostic rules
- **Symptoms Tracked:** 20+ clinical signs
- **Knowledge Sources:** 25 curated medical documents
- **API Endpoints:** 9 endpoints
- **LLM Models Supported:** 4 (Llama 3.3, Llama 3.1, Mixtral, Gemma)

---

## 2. Project Goals & Objectives

### 2.1 Primary Goals

| Goal | Description | Status |
|------|-------------|--------|
| G1 | Create rule-based expert system for tropical disease diagnosis | ✅ Complete |
| G2 | Implement WHO dehydration classification protocol | ✅ Complete |
| G3 | Provide AI-powered conversational interface | ✅ Complete |
| G4 | Build extensible architecture for adding diseases | ✅ Complete |
| G5 | Create comprehensive API documentation | ✅ Complete |

### 2.2 Secondary Goals

| Goal | Description | Status |
|------|-------------|--------|
| S1 | Support multiple LLM providers/models | ✅ Complete |
| S2 | Implement knowledge retrieval (RAG) | ✅ Complete |
| S3 | Docker containerization | ✅ Complete |
| S4 | Production deployment guide | 🔄 Partial |

### 2.3 Success Criteria

1. **Accuracy:** Expert system produces clinically valid diagnoses for test cases
2. **Usability:** API is well-documented and easy to integrate
3. **Performance:** Response time < 2 seconds for expert system, < 10 seconds for AI chat
4. **Extensibility:** New diseases can be added without architectural changes

### 2.4 Non-Goals (Explicit Exclusions)

- ❌ This is NOT a certified medical device
- ❌ NOT intended for autonomous diagnosis without clinician oversight
- ❌ NOT a replacement for laboratory confirmation
- ❌ NOT designed for emergency triage (life-threatening conditions)

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT APPLICATIONS                          │
│                  (Web App, Mobile App, Chatbots)                    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         API GATEWAY LAYER                           │
│                        (Django Ninja API)                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  /api/expert/*   │  │   /api/chat/*    │  │  /api/ping, /    │  │
│  │  Expert Router   │  │   Chat Router    │  │  Health Checks   │  │
│  └────────┬─────────┘  └────────┬─────────┘  └──────────────────┘  │
└───────────┼─────────────────────┼───────────────────────────────────┘
            │                     │
            ▼                     ▼
┌───────────────────────┐  ┌─────────────────────────────────────────┐
│   EXPERT SYSTEM CORE  │  │           AI SERVICE LAYER              │
│   ┌─────────────────┐ │  │  ┌─────────────┐  ┌─────────────────┐  │
│   │ DiagnosisEngine │ │  │  │ LLM Client  │  │ Knowledge Base  │  │
│   │   (Experta)     │ │  │  │   (Groq)    │  │     (RAG)       │  │
│   ├─────────────────┤ │  │  └──────┬──────┘  └────────┬────────┘  │
│   │    50+ Rules    │ │  │         │                  │           │
│   │  WHO Protocols  │ │  │         ▼                  ▼           │
│   └─────────────────┘ │  │  ┌─────────────────────────────────┐   │
└───────────────────────┘  │  │      Prompt Engineering         │   │
                           │  │  (System Prompt + Expert Rules) │   │
                           │  └─────────────────────────────────┘   │
                           └─────────────────────────────────────────┘
                                          │
                                          ▼
                           ┌─────────────────────────────────────────┐
                           │           EXTERNAL SERVICES             │
                           │  ┌─────────────────────────────────┐   │
                           │  │         Groq API                │   │
                           │  │  (Llama 3.3, Mixtral, Gemma)    │   │
                           │  └─────────────────────────────────┘   │
                           └─────────────────────────────────────────┘
```

### 3.2 Component Architecture

```
src/
├── config/                    # Django Configuration Layer
│   ├── settings.py           # Environment-aware settings
│   ├── urls.py               # URL routing to API
│   ├── wsgi.py               # Sync WSGI entry point
│   └── asgi.py               # Async ASGI entry point
│
├── api/                       # API Presentation Layer
│   ├── api.py                # NinjaAPI initialization
│   ├── routers/
│   │   ├── expert.py         # Expert system endpoints
│   │   └── chat.py           # AI chat endpoints
│   └── schemas/
│       ├── expert.py         # Pydantic models (expert)
│       └── chat.py           # Pydantic models (chat)
│
└── lib/                       # Business Logic Layer
    ├── expert_system/         # Rule-Based Engine
    │   ├── diagnosis_engine.py   # Experta KnowledgeEngine
    │   ├── facts.py              # Fact definitions
    │   ├── main.py               # CLI interface
    │   └── raw_knowledge/        # Medical knowledge files
    │
    └── ai/                    # AI/LLM Integration
        ├── llm_client.py      # Groq API client
        ├── knowledge_base.py  # RAG retrieval
        └── prompts.py         # Prompt engineering
```

### 3.3 Layer Responsibilities

| Layer | Components | Responsibility |
|-------|------------|----------------|
| **Presentation** | Django Ninja, Routers, Schemas | HTTP handling, validation, serialization |
| **Business Logic** | Expert System, AI Service | Core diagnostic logic, LLM orchestration |
| **Data Access** | Knowledge Base, Facts | Medical knowledge retrieval, fact management |
| **External Services** | Groq API | LLM inference |

### 3.4 Design Patterns Used

| Pattern | Application |
|---------|-------------|
| **Repository** | KnowledgeBase abstracts knowledge file access |
| **Strategy** | LLMClient supports multiple model backends |
| **Factory** | run_diagnosis() creates and configures engine |
| **Facade** | API routers simplify access to complex subsystems |
| **Singleton** | Global KnowledgeBase instance for performance |

---

## 4. Technology Stack & Rationale

### 4.1 Core Technologies

| Technology | Version | Purpose | Rationale |
|------------|---------|---------|-----------|
| **Python** | 3.8.x | Runtime | Required for Experta compatibility (collections.Mapping) |
| **Django** | 4.2 LTS | Web Framework | Mature, well-documented, LTS support |
| **Django Ninja** | 1.5+ | API Framework | Fast, Pydantic-native, auto OpenAPI docs |
| **Experta** | 1.9.4 | Expert System | Python CLIPS port, production rules |
| **Pydantic** | 2.x | Validation | Type-safe request/response models |
| **httpx** | 0.28+ | HTTP Client | Async support for LLM API calls |

### 4.2 AI/LLM Stack

| Technology | Purpose | Rationale |
|------------|---------|-----------|
| **Groq API** | LLM Provider | Free tier, fast inference, OpenAI-compatible |
| **Llama 3.3 70B** | Default Model | Best reasoning for medical domain |
| **Mixtral 8x7B** | Alternative | Good balance of speed/quality |
| **Gemma 2 9B** | Lightweight | Fast responses, smaller context |

### 4.3 Alternative Technologies Considered

| Category | Chosen | Alternatives Considered | Reason for Choice |
|----------|--------|------------------------|-------------------|
| API Framework | Django Ninja | FastAPI, DRF | Django ecosystem, Pydantic integration |
| Expert System | Experta | PyKE, Drools | Pure Python, active maintenance |
| LLM Provider | Groq | OpenAI, Anthropic, Local | Free tier, speed, no GPU required |
| Vector DB | None (keyword RAG) | Pinecone, ChromaDB | Simplicity for MVP, can upgrade |

### 4.4 Python 3.8 Constraint

**Why Python 3.8 specifically:**

```python
# Experta uses this import pattern:
from collections import Mapping  # Removed in Python 3.10

# Python 3.9: DeprecationWarning
# Python 3.10+: AttributeError: module 'collections' has no attribute 'Mapping'
```

**Implications:**
- Type hints use `List[str]` not `list[str]` (PEP 585 not fully supported)
- Some newer library features unavailable
- Docker must use `python:3.8-slim` base image

---

## 5. Expert System Design

### 5.1 Knowledge Representation

The expert system uses **Experta's Fact-based representation**:

```python
# Facts represent observable data
class Symptom(Fact):
    """
    Fields:
        name: str - Symptom identifier
        present: bool - Is symptom present
        severity: str - mild/moderate/severe
        pattern: str - cyclical/stepladder/continuous
        description: str - Additional details
    """
    pass

class Patient(Fact):
    """
    Fields:
        age: int
        travel_endemic_area: bool
        unsafe_water: bool
        ...
    """
    pass
```

### 5.2 Rule Structure

Rules follow the **Production Rule** paradigm:

```
IF <conditions> THEN <actions>
```

**Example Rule:**
```python
@Rule(
    Symptom(name='fever', present=True, pattern='cyclical'),
    Symptom(name='chills', present=True),
    Symptom(name='sweating', present=True),
    salience=90  # Priority
)
def malaria_confident_paroxysm(self):
    """Classic malarial paroxysm = confident malaria diagnosis"""
    self.declare(Diagnosis(
        disease='malaria',
        confidence='confident',
        reason='classic malarial paroxysm'
    ))
```

### 5.3 Rule Categories

| Category | Count | Description |
|----------|-------|-------------|
| **Dehydration Classification** | 3 | WHO Plans A/B/C |
| **Cholera Rules** | 8 | Rice-water stool, AWD, lab confirmation |
| **Malaria Rules** | 12 | Paroxysm, bitter taste, species-specific |
| **Typhoid Rules** | 10 | Stepladder fever, rose spots, bradycardia |
| **Severity Indicators** | 8 | Danger signs, urgent referral |
| **Differential Diagnosis** | 5 | Rule-out logic |

### 5.4 Confidence Level System

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONFIDENCE HIERARCHY                         │
├─────────────────────────────────────────────────────────────────┤
│  CONFIRMED (100%)    │ Laboratory-verified diagnosis            │
│  ──────────────────  │ - Positive blood smear (malaria)         │
│                      │ - Positive stool culture (cholera)       │
│                      │ - Positive blood culture (typhoid)       │
├─────────────────────────────────────────────────────────────────┤
│  CONFIDENT (85-95%)  │ Pathognomonic clinical signs             │
│  ──────────────────  │ - Rice-water stool (cholera)             │
│                      │ - Classic paroxysm (malaria)             │
│                      │ - Stepladder fever + bradycardia         │
├─────────────────────────────────────────────────────────────────┤
│  SUSPECT (50-75%)    │ Clinical suspicion + epidemiology        │
│  ──────────────────  │ - Fever + endemic area travel            │
│                      │ - AWD + unsafe water exposure            │
│                      │ - Prolonged fever + GI symptoms          │
├─────────────────────────────────────────────────────────────────┤
│  UNCERTAIN (10-25%)  │ Insufficient findings                    │
│  ──────────────────  │ - Non-specific symptoms only             │
│                      │ - No exposure history                    │
│                      │ - Conflicting indicators                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.5 WHO Dehydration Protocol Implementation

```
┌────────────────────────────────────────────────────────────────────┐
│                WHO DEHYDRATION ASSESSMENT                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Assess:  Mental State → Eyes → Skin Pinch → Thirst               │
│                                                                    │
│  ┌─────────────────┬─────────────────┬─────────────────┐          │
│  │   NO DEHYDRATION │  SOME DEHYDRATION │ SEVERE DEHYDRATION │     │
│  │   (Plan A)       │   (Plan B)        │   (Plan C)         │     │
│  ├─────────────────┼─────────────────┼─────────────────┤          │
│  │ Alert           │ Restless/        │ Lethargic/      │          │
│  │                 │ Irritable        │ Unconscious     │          │
│  ├─────────────────┼─────────────────┼─────────────────┤          │
│  │ Normal eyes     │ Sunken eyes      │ Sunken eyes     │          │
│  ├─────────────────┼─────────────────┼─────────────────┤          │
│  │ Normal pinch    │ Slow pinch       │ Very slow >2s   │          │
│  ├─────────────────┼─────────────────┼─────────────────┤          │
│  │ Drinks normally │ Drinks eagerly   │ Unable to drink │          │
│  ├─────────────────┼─────────────────┼─────────────────┤          │
│  │ HOME FLUIDS     │ ORS THERAPY      │ IV FLUIDS       │          │
│  │                 │ 4-6 hours        │ URGENT          │          │
│  └─────────────────┴─────────────────┴─────────────────┘          │
└────────────────────────────────────────────────────────────────────┘
```

### 5.6 Salience (Priority) System

Rules have priorities (salience) to control firing order:

| Salience | Rule Type | Example |
|----------|-----------|---------|
| 100 | Lab-confirmed diagnosis | Positive blood culture |
| 95 | Positive RDT | Malaria RDT positive |
| 90 | Pathognomonic signs | Rice-water stool |
| 85 | High-confidence clinical | Classic paroxysm |
| 70-80 | Strong clinical suspicion | Fever + endemic + symptoms |
| 50-65 | Moderate suspicion | Non-specific + exposure |
| 10-25 | Weak/uncertain | Fallback rules |

---

## 6. AI Integration Layer

### 6.1 Architecture Philosophy

The AI layer follows the **"AI as Advisor"** pattern:

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI ADVISOR PATTERN                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Expert System Rules  ──┐                                       │
│                         │                                       │
│  Knowledge Base (RAG) ──┼──▶ System Prompt ──▶ LLM ──▶ Response │
│                         │                                       │
│  User Message ──────────┘                                       │
│                                                                 │
│  The AI REFERENCES expert rules, doesn't just wrap them.        │
│  It can reason beyond the rules while staying grounded.         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 LLM Client Design

```python
class LLMClient:
    """
    Async client for Groq's OpenAI-compatible API.
    
    Features:
    - Model switching at runtime
    - Streaming support (future)
    - Automatic retry logic
    - Token usage tracking (future)
    """
    
    async def chat(
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False
    ) -> str
```

### 6.3 Supported Models

| Model ID | Context | Speed | Quality | Best For |
|----------|---------|-------|---------|----------|
| `llama-3.3-70b-versatile` | 128K | Medium | Excellent | Complex reasoning |
| `llama-3.1-8b-instant` | 128K | Fast | Good | Quick responses |
| `mixtral-8x7b-32768` | 32K | Medium | Very Good | Balanced |
| `gemma2-9b-it` | 8K | Fast | Good | Simple queries |

### 6.4 Prompt Engineering Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    SYSTEM PROMPT STRUCTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ROLE DEFINITION                                             │
│     "You are a Medical Diagnostic Assistant..."                 │
│                                                                 │
│  2. CAPABILITIES & LIMITATIONS                                  │
│     - Can analyze: Cholera, Malaria, Typhoid                   │
│     - Cannot: Provide definitive diagnosis                      │
│                                                                 │
│  3. DANGER SIGNS (Always highlight)                             │
│     - Altered consciousness                                     │
│     - Severe dehydration                                        │
│     - Bloody symptoms                                           │
│                                                                 │
│  4. EXPERT SYSTEM RULES SUMMARY                                 │
│     [Embedded diagnostic criteria from diagnosis_engine.py]     │
│                                                                 │
│  5. CONVERSATION GUIDELINES                                     │
│     - Ask clarifying questions                                  │
│     - Systematic symptom assessment                             │
│     - Always recommend professional evaluation                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.5 Knowledge Base RAG

**Retrieval Strategy:**

```
User Query: "I have fever and chills after visiting Nigeria"
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  SYMPTOM EXTRACTION                                             │
│  ─────────────────                                              │
│  Detected: ["fever", "chills"]                                  │
│  Travel: Nigeria → endemic area                                 │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  KNOWLEDGE RETRIEVAL                                            │
│  ───────────────────                                            │
│  1. Score chunks by keyword overlap                             │
│  2. Boost scores for matching diseases                          │
│  3. Return top 3-5 relevant chunks                              │
└─────────────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  CONTEXT INJECTION                                              │
│  ─────────────────                                              │
│  Retrieved: malaria1.md (paroxysm section)                      │
│            malaria3.md (endemic travel section)                 │
│  Injected into user message context                             │
└─────────────────────────────────────────────────────────────────┘
```

### 6.6 Symptom Extraction

The chat router extracts symptoms from natural language:

```python
SYMPTOM_KEYWORDS = {
    "fever": ["fever", "febrile", "temperature", "hot"],
    "chills": ["chills", "rigors", "shivering"],
    "diarrhea": ["diarrhea", "loose stool", "watery stool"],
    # ...
}

def extract_symptoms_from_text(text: str) -> List[str]:
    """Simple keyword matching for symptom extraction."""
```

**Future Enhancement:** Use NER model for better extraction.

---

## 7. API Design & Endpoints

### 7.1 API Design Principles

| Principle | Implementation |
|-----------|----------------|
| **RESTful** | Resource-based URLs, HTTP verbs |
| **Consistent** | Standard response formats |
| **Documented** | OpenAPI/Swagger auto-generated |
| **Validated** | Pydantic models for all I/O |
| **Versioned** | `/api/` prefix (v2 would be `/api/v2/`) |

### 7.2 Endpoint Summary

```
/api/
├── GET  /                      # API info
├── GET  /ping                  # Health check
├── GET  /docs                  # Swagger UI
│
├── /expert/
│   ├── POST /diagnose          # Run expert diagnosis
│   ├── GET  /symptoms          # List valid symptoms
│   ├── GET  /diseases          # List diseases
│   └── GET  /diseases/{name}   # Get disease details
│
└── /chat/
    ├── POST /message           # Send chat message
    ├── GET  /models            # List LLM models
    └── POST /validate-model    # Validate model ID
```

### 7.3 Response Format Standards

**Success Response:**
```json
{
  "diagnoses": [...],
  "recommendations": [...],
  "disclaimer": "..."
}
```

**Error Response:**
```json
{
  "detail": "Error message"
}
```

**Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "symptoms", 0, "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## 8. Data Flow & Sequence Diagrams

### 8.1 Expert System Diagnosis Flow

```
┌────────┐          ┌─────────┐          ┌────────────┐          ┌───────────┐
│ Client │          │  Router │          │ run_diag() │          │  Experta  │
└───┬────┘          └────┬────┘          └─────┬──────┘          └─────┬─────┘
    │                    │                     │                       │
    │  POST /diagnose    │                     │                       │
    │  {symptoms:[...]}  │                     │                       │
    │───────────────────▶│                     │                       │
    │                    │                     │                       │
    │                    │  Validate Request   │                       │
    │                    │  (Pydantic)         │                       │
    │                    │─────────────────────│                       │
    │                    │                     │                       │
    │                    │  run_diagnosis()    │                       │
    │                    │────────────────────▶│                       │
    │                    │                     │                       │
    │                    │                     │  engine.reset()       │
    │                    │                     │──────────────────────▶│
    │                    │                     │                       │
    │                    │                     │  declare(facts)       │
    │                    │                     │──────────────────────▶│
    │                    │                     │                       │
    │                    │                     │  engine.run()         │
    │                    │                     │──────────────────────▶│
    │                    │                     │                       │
    │                    │                     │         ◀─────────────│
    │                    │                     │     Rules Fire        │
    │                    │                     │     (Rete Algorithm)  │
    │                    │                     │                       │
    │                    │                     │  get_diagnoses()      │
    │                    │                     │──────────────────────▶│
    │                    │                     │                       │
    │                    │     {diagnoses}     │◀──────────────────────│
    │                    │◀────────────────────│                       │
    │                    │                     │                       │
    │   DiagnoseResponse │                     │                       │
    │◀───────────────────│                     │                       │
    │                    │                     │                       │
```

### 8.2 AI Chat Flow

```
┌────────┐     ┌─────────┐     ┌───────────┐     ┌──────────┐     ┌──────────┐
│ Client │     │  Router │     │ Knowledge │     │  Prompt  │     │ Groq API │
└───┬────┘     └────┬────┘     │   Base    │     │  Builder │     └────┬─────┘
    │               │          └─────┬─────┘     └────┬─────┘          │
    │               │                │                │                │
    │ POST /message │                │                │                │
    │ {message,     │                │                │                │
    │  history:[]}  │                │                │                │
    │──────────────▶│                │                │                │
    │               │                │                │                │
    │               │ extract_symptoms()             │                │
    │               │────────────────│                │                │
    │               │                │                │                │
    │               │ get_relevant_context()         │                │
    │               │───────────────▶│                │                │
    │               │                │                │                │
    │               │   [chunks]     │                │                │
    │               │◀───────────────│                │                │
    │               │                │                │                │
    │               │ build_system_prompt()          │                │
    │               │───────────────────────────────▶│                │
    │               │                │                │                │
    │               │   system_prompt               │                │
    │               │◀───────────────────────────────│                │
    │               │                │                │                │
    │               │ LLMClient.chat([messages])     │                │
    │               │────────────────────────────────────────────────▶│
    │               │                │                │                │
    │               │                │                │    LLM        │
    │               │                │                │  Inference    │
    │               │                │                │                │
    │               │              response_text     │                │
    │               │◀────────────────────────────────────────────────│
    │               │                │                │                │
    │ ChatResponse  │                │                │                │
    │ {response,    │                │                │                │
    │  history,     │                │                │                │
    │  extracted}   │                │                │                │
    │◀──────────────│                │                │                │
```

### 8.3 Conversation State Management

```
┌─────────────────────────────────────────────────────────────────────┐
│                  STATELESS CONVERSATION FLOW                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Request 1:                                                         │
│  ─────────                                                          │
│  {                                                                  │
│    "message": "I have a fever",                                     │
│    "conversation_history": []                                       │
│  }                                                                  │
│                                                                     │
│  Response 1:                                                        │
│  ──────────                                                         │
│  {                                                                  │
│    "response": "I'm sorry to hear that...",                        │
│    "conversation_history": [                                        │
│      {"role": "user", "content": "I have a fever"},                │
│      {"role": "assistant", "content": "I'm sorry..."}              │
│    ]                                                                │
│  }                                                                  │
│                                                                     │
│  Request 2 (include history from Response 1):                       │
│  ─────────                                                          │
│  {                                                                  │
│    "message": "Also having chills",                                 │
│    "conversation_history": [                                        │
│      {"role": "user", "content": "I have a fever"},                │
│      {"role": "assistant", "content": "I'm sorry..."}              │
│    ]                                                                │
│  }                                                                  │
│                                                                     │
│  Client stores history, server is stateless.                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 9. Knowledge Base Structure

### 9.1 Raw Knowledge Organization

```
src/lib/expert_system/raw_knowledge/
├── cholera/
│   ├── cholera1.md    # Pathophysiology & transmission
│   ├── cholera2.md    # Clinical presentation
│   ├── cholera3.md    # WHO treatment protocols
│   ├── cholera4.md    # Laboratory diagnosis
│   └── cholera5.md    # Prevention & outbreak response
│
├── malaria/
│   ├── malaria1.md    # Diagnostic logic tree
│   ├── malaria2.md    # Species-specific features
│   ├── malaria3.md    # Severe malaria criteria
│   ├── malaria4.md    # Treatment protocols (ACT)
│   ├── malaria5.md    # Pediatric considerations
│   ├── malaria6.md    # Pregnancy considerations
│   ├── malaria7.md    # Drug resistance
│   ├── malaria8.md    # Differential diagnosis
│   ├── malaria9.md    # Prevention (prophylaxis)
│   ├── malaria10.md   # Co-infections
│   └── malaria11.md   # Lab interpretation
│
└── typhoid_fever/
    ├── typhoid_fever1.md   # Epidemiology
    ├── typhoid_fever2.md   # Clinical features
    ├── typhoid_fever3.md   # Diagnostic approach
    ├── typhoid_fever4.md   # Widal test interpretation
    ├── typhoid_fever5.md   # Treatment protocols
    ├── typhoid_fever6.md   # Complications
    ├── typhoid_fever7.md   # Carrier state
    ├── typhoid_fever8.md   # Pediatric typhoid
    └── typhoid_fever9.md   # Drug resistance
```

### 9.2 Knowledge File Format

Each markdown file follows a structured format:

```markdown
### Section Title

**Key Point**
- Bullet points for clarity

**Logic Rule:**
IF (condition1) AND (condition2)
THEN action/classification

**Clinical Pearl:**
Important clinical insight for practitioners.

**References:**
- WHO guidelines
- Clinical studies
```

### 9.3 Knowledge Indexing

```python
class KnowledgeChunk:
    disease: str          # "Malaria", "Cholera", "Typhoid Fever"
    source_file: str      # "malaria1.md"
    title: str            # Section heading
    content: str          # Raw markdown content
    keywords: Set[str]    # Extracted medical keywords
```

---

## 10. Security Considerations

### 10.1 Current Security Measures

| Measure | Status | Implementation |
|---------|--------|----------------|
| Input Validation | ✅ | Pydantic schemas |
| CORS | ✅ | django-cors-headers |
| Secret Management | ✅ | Environment variables |
| SQL Injection | ✅ | Django ORM (no raw SQL) |
| XSS | N/A | API-only, no HTML rendering |

### 10.2 Security Recommendations (Production)

| Recommendation | Priority | Notes |
|----------------|----------|-------|
| HTTPS | 🔴 Critical | Use TLS in production |
| Rate Limiting | 🔴 Critical | Protect AI endpoints from abuse |
| API Key Auth | 🟡 High | Authenticate API consumers |
| Input Sanitization | 🟡 High | Sanitize AI chat input |
| Audit Logging | 🟡 High | Log all diagnosis requests |
| CORS Whitelist | 🟡 High | Restrict origins in production |

### 10.3 API Key Protection

```python
# Current: API key in .env file
GROQ_API_KEY=gsk_xxxxx

# Production: Use secrets manager
# - AWS Secrets Manager
# - Azure Key Vault
# - HashiCorp Vault
```

### 10.4 Medical Data Privacy

**Important Considerations:**
- No patient data is stored by the API (stateless)
- Conversation history sent by client (client responsibility)
- LLM requests sent to Groq (third-party)
- For HIPAA compliance, consider self-hosted LLM

---

## 11. Performance Considerations

### 11.1 Current Performance Characteristics

| Operation | Typical Latency | Bottleneck |
|-----------|-----------------|------------|
| Expert Diagnosis | 50-200ms | Rule evaluation |
| AI Chat | 2-8 seconds | LLM inference |
| Knowledge Retrieval | 10-50ms | File I/O (first load) |
| Symptom List | <10ms | Static data |

### 11.2 Optimization Strategies

**Implemented:**
- Singleton KnowledgeBase (loaded once)
- Async HTTP client for LLM calls
- Minimal database queries (SQLite for Django internals only)

**Recommended (Future):**
- Redis caching for knowledge chunks
- Vector embeddings for faster RAG
- Response streaming for AI chat
- Connection pooling for high concurrency

### 11.3 Scalability Considerations

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SCALING ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Current (Single Instance):                                         │
│  ─────────────────────────                                          │
│  Django Runserver ──▶ Single Process                                │
│                                                                     │
│  Production (Scaled):                                               │
│  ───────────────────                                                │
│                                                                     │
│  Load Balancer                                                      │
│       │                                                             │
│       ├──▶ Container 1 (Uvicorn + Django)                          │
│       ├──▶ Container 2 (Uvicorn + Django)                          │
│       └──▶ Container 3 (Uvicorn + Django)                          │
│                    │                                                │
│                    └──▶ Shared Redis Cache                          │
│                                                                     │
│  Expert system is CPU-bound (can scale horizontally)                │
│  AI chat is I/O-bound (async handles concurrency well)              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 12. Testing Strategy

### 12.1 Test Categories

| Category | Coverage | Tools |
|----------|----------|-------|
| Unit Tests | Expert system rules | pytest, Django TestCase |
| Integration Tests | API endpoints | Django test client |
| E2E Tests | Full diagnosis flow | httpx, pytest |
| Manual Testing | AI chat quality | Swagger UI |

### 12.2 Expert System Test Cases

```python
# Test: Classic malaria paroxysm
def test_malaria_paroxysm():
    result = run_diagnosis(symptoms=[
        {"name": "fever", "present": True, "pattern": "cyclical"},
        {"name": "chills", "present": True},
        {"name": "sweating", "present": True},
    ])
    assert any(d["disease"] == "malaria" and d["confidence"] == "confident" 
               for d in result["diagnoses"])

# Test: Rice-water stool → Cholera
def test_cholera_ricewater():
    result = run_diagnosis(symptoms=[
        {"name": "diarrhea", "present": True, "description": "rice_water"},
    ])
    assert any(d["disease"] == "cholera" and d["confidence"] == "confident"
               for d in result["diagnoses"])
```

### 12.3 Test Data Sets

Pre-defined scenarios in `main.py --test`:

| Scenario | Expected Diagnosis | Confidence |
|----------|-------------------|------------|
| Classic malaria | Malaria | Confident |
| Rice-water diarrhea | Cholera | Confident |
| Stepladder fever + bradycardia | Typhoid | Confident |
| Non-specific fever | Multiple suspects | Suspect |
| Lab-confirmed malaria | Malaria | Confirmed |

---

## 13. Deployment Architecture

### 13.1 Docker Configuration

**Dockerfile:**
```dockerfile
FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "src.config.asgi:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 13.2 Docker Compose (Development)

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - DJANGO_DEBUG=True
    volumes:
      - .:/app
```

### 13.3 Production Deployment Options

| Platform | Pros | Cons |
|----------|------|------|
| **Railway** | Easy deploy, free tier | Limited resources |
| **Render** | Auto-deploy from Git | Cold starts |
| **Fly.io** | Global edge, containers | Complex config |
| **AWS ECS** | Scalable, production-ready | Complex, costly |
| **Vercel** | Serverless Django | Limited for long AI requests |

### 13.4 Environment Variables

```bash
# Required
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx

# Optional
OPEN_API_BASE_URL=https://api.groq.com/openai/v1
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-production-secret
ALLOWED_HOSTS=yourdomain.com
```

---

## 14. Future Roadmap

### 14.1 Phase 2: Enhanced Features (Q1 2026)

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| Additional Diseases | 🔴 High | Medium | Dengue, Typhus, Yellow Fever |
| Conversation Persistence | 🔴 High | Medium | Database storage for chat history |
| User Authentication | 🟡 Medium | Medium | JWT-based auth |
| Streaming Responses | 🟡 Medium | Low | SSE for AI chat |
| Vector Embeddings RAG | 🟡 Medium | High | Replace keyword search |

### 14.2 Phase 3: Production Hardening (Q2 2026)

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| Rate Limiting | 🔴 High | Low | Redis-based throttling |
| Monitoring & Alerts | 🔴 High | Medium | Prometheus, Grafana |
| Audit Logging | 🔴 High | Medium | All diagnosis events |
| Load Testing | 🟡 Medium | Medium | k6 or Locust |
| Multi-language | 🟡 Medium | High | i18n support |

### 14.3 Phase 4: Advanced Features (Q3-Q4 2026)

| Feature | Priority | Effort | Description |
|---------|----------|--------|-------------|
| Self-hosted LLM | 🟡 Medium | High | Ollama/vLLM integration |
| Image Analysis | 🟢 Low | High | Rash/stool photo analysis |
| Voice Input | 🟢 Low | Medium | Speech-to-text integration |
| Mobile SDK | 🟢 Low | High | iOS/Android native libraries |
| Admin Dashboard | 🟡 Medium | Medium | Django admin customization |

### 14.4 Technical Debt

| Item | Priority | Notes |
|------|----------|-------|
| Python 3.8 constraint | 🟡 Medium | Fork/patch Experta for 3.10+ |
| Sync expert system | 🟢 Low | Consider async Experta fork |
| Keyword RAG | 🟡 Medium | Upgrade to embeddings |
| No test coverage metrics | 🟡 Medium | Add pytest-cov |

---

## 15. Known Limitations

### 15.1 Technical Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Python 3.8 only | No new language features | Document clearly |
| Experta not async | Blocks event loop briefly | Fast enough for now |
| Keyword-based RAG | Less semantic accuracy | Upgrade to embeddings |
| No offline mode | Requires internet for AI | Expert system works offline |
| Groq rate limits | May fail under load | Implement retry logic |

### 15.2 Clinical Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Only 3 diseases | Limited scope | Designed for expansion |
| No image input | Can't assess rashes, stool | Future enhancement |
| English only | Limited accessibility | i18n planned |
| No pediatric dosing | Treatment guidance limited | Recommend clinician |
| No drug interactions | Safety concern | Always recommend professional review |

### 15.3 Disclaimer

```
⚠️ IMPORTANT LIMITATIONS

This system is designed as a CLINICAL DECISION SUPPORT tool, NOT a 
replacement for professional medical judgment. 

- NOT a certified medical device
- NOT validated for clinical use
- NOT suitable for emergency triage
- Laboratory confirmation ALWAYS required for definitive diagnosis

All diagnostic suggestions must be validated by a qualified 
healthcare professional before any treatment decisions are made.
```

---

## 16. Appendices

### Appendix A: Full Symptom Reference

| Symptom | Type | Options | Associated Diseases |
|---------|------|---------|---------------------|
| fever | Core | pattern, severity, duration | All |
| chills | Core | - | Malaria |
| sweating | Core | - | Malaria |
| diarrhea | GI | description, severity | Cholera, Typhoid |
| vomiting | GI | severity | Cholera |
| dehydration | GI | severity | Cholera |
| headache | Neuro | severity | Malaria, Typhoid |
| abdominal_pain | GI | severity | Typhoid |
| severe_abdominal_pain | GI | - | Typhoid (danger) |
| constipation | GI | - | Typhoid |
| bitter_taste | Oral | - | Malaria |
| rose_spots | Skin | - | Typhoid |
| relative_bradycardia | Cardiac | - | Typhoid |
| altered_consciousness | Neuro | - | All (danger) |
| convulsions | Neuro | - | Malaria (danger) |
| body_aches | MSK | - | Malaria |
| dark_urine | Renal | description | Malaria (danger) |
| anemia | Heme | severity | Malaria |
| melena | GI | - | Typhoid (danger) |
| bloody_stool | GI | - | Typhoid (danger) |

### Appendix B: Lab Test Reference

| Test | Disease | Positive Criteria | Confidence |
|------|---------|-------------------|------------|
| blood_smear | Malaria | Plasmodium seen | Confirmed |
| rdt_malaria | Malaria | Positive band | Confident |
| stool_culture | Cholera | V. cholerae isolated | Confirmed |
| rdt_cholera | Cholera | Positive band | Confident |
| blood_culture | Typhoid | S. typhi isolated | Confirmed |
| widal | Typhoid | Titer ≥1:160 | Suspect-Confident |
| typhidot | Typhoid | IgM positive | Confident |

### Appendix C: API Response Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Diagnosis returned |
| 400 | Bad Request | Invalid JSON |
| 404 | Not Found | Disease not found |
| 422 | Validation Error | Missing required field |
| 500 | Server Error | LLM API failure |
| 503 | Service Unavailable | Groq API down |

### Appendix D: Configuration Reference

```python
# Django Settings (src/config/settings.py)
DJANGO_SETTINGS_MODULE = 'src.config.settings'
DEBUG = True  # Set False in production
ALLOWED_HOSTS = []  # Add domain in production

# AI Configuration (src/lib/ai/llm_client.py)
DEFAULT_MODEL = 'llama-3.3-70b-versatile'
TEMPERATURE = 0.7
MAX_TOKENS = 2048

# Expert System (src/lib/expert_system/diagnosis_engine.py)
# Salience ranges: 10-100 (higher = fires first)
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-08 | System | Initial comprehensive report |

---

**End of Project Report**
