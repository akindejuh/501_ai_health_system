# MESA - Medical Expert System Assistant

## Project Summary & Defense Guide

---

## Table of Contents

1. [What Is This Project?](#1-what-is-this-project)
2. [The Problem It Solves](#2-the-problem-it-solves)
3. [How the Project Was Built (Development Approach)](#3-how-the-project-was-built-development-approach)
4. [How It Works (Non-Technical)](#4-how-it-works-non-technical)
5. [Technology Stack & Why Each Was Chosen](#5-technology-stack--why-each-was-chosen)
6. [Project Structure (File-by-File Walkthrough)](#6-project-structure-file-by-file-walkthrough)
7. [The Two Brains: Expert System vs AI Chat](#7-the-two-brains-expert-system-vs-ai-chat)
8. [How Data Flows Through the System](#8-how-data-flows-through-the-system)
9. [The Expert System (Rule Engine) Explained](#9-the-expert-system-rule-engine-explained)
10. [The AI Chat System Explained](#10-the-ai-chat-system-explained)
11. [The Frontend (What Users See)](#11-the-frontend-what-users-see)
12. [API Endpoints (How Frontend Talks to Backend)](#12-api-endpoints-how-frontend-talks-to-backend)
13. [The Knowledge Base (Medical Data)](#13-the-knowledge-base-medical-data)
14. [Deployment & Infrastructure](#14-deployment--infrastructure)
15. [Security & Ethical Considerations](#15-security--ethical-considerations)
16. [Limitations & Future Work](#16-limitations--future-work)

---

## 1. What Is This Project?

MESA is a **web-based medical diagnostic assistance tool** that helps healthcare workers assess patients for three tropical diseases:

- **Cholera**
- **Malaria**
- **Typhoid Fever**

It has **two modes**:

| Mode | How It Works | Analogy |
|------|-------------|---------|
| **Expert Mode** | User selects symptoms from a checklist, system applies medical rules to produce a diagnosis | Like filling out a medical form — structured, predictable |
| **Chat Mode** | User describes symptoms in natural language, an AI assistant asks follow-up questions and gives assessments | Like texting a knowledgeable medical assistant — conversational, flexible |

**In simple terms**: Think of it as a smart medical assistant that can either work like a structured questionnaire (Expert Mode) or have a conversation with you about symptoms (Chat Mode).

---

## 2. The Problem It Solves

In many tropical regions:
- Access to specialists is limited
- Diseases like malaria, cholera, and typhoid are common but share overlapping symptoms
- Healthcare workers need quick guidance on what disease they might be dealing with

MESA provides a **decision support tool** — it doesn't replace doctors, but helps healthcare workers make faster, more informed assessments by:
- Following WHO (World Health Organization) protocols
- Applying established diagnostic rules
- Giving confidence levels (confirmed, suspected, uncertain)
- Flagging danger signs that need immediate attention

---

## 3. How the Project Was Built (Development Approach)

### The Big Picture Approach

This project was built using a **modular, layered architecture** — meaning each piece was developed independently and then connected together. The development followed roughly this order:

### Phase 1: Research & Knowledge Gathering

**What happened**: Before writing any code, medical knowledge about the three target diseases (cholera, malaria, typhoid) was compiled into structured Markdown files.

**Files created**:

- `backend/src/lib/expert_system/raw_knowledge/cholera/` — 5 files
- `backend/src/lib/expert_system/raw_knowledge/malaria/` — 11 files
- `backend/src/lib/expert_system/raw_knowledge/typhoid_fever/` — 9 files

**Why this step matters**: The entire system is only as good as its medical knowledge. These 25 files serve as the foundation — they feed both the expert system rules and the AI chat's knowledge retrieval.

### Phase 2: Expert System (The Rule Engine)

**What happened**: The core diagnostic logic was built using Experta, a Python rule engine. Medical knowledge from Phase 1 was translated into IF-THEN rules with priority levels.

**Files created (in order)**:

1. `backend/src/lib/expert_system/facts.py` — Defined the data structures (what a "Symptom", "Patient", "LabResult" looks like in the system)
2. `backend/src/lib/expert_system/diagnosis_engine.py` — The main engine: 650+ lines of diagnostic rules covering all three diseases, plus the WHO dehydration classification
3. `backend/src/lib/expert_system/main.py` — A command-line interface to test the engine directly without needing a web server

**Why this approach**: Rule-based expert systems are the traditional approach for medical decision support. They are **transparent** (you can see exactly why a diagnosis was made), **auditable** (important in healthcare), and **deterministic** (same inputs always give same outputs).

### Phase 3: Backend API Setup

**What happened**: A Django project was set up with Django Ninja for the REST API. This wraps the expert system in a web API that the frontend can call.

**Files created (in order)**:

1. `backend/src/config/settings.py` — Django configuration (database, CORS, security settings)
2. `backend/src/config/urls.py` — URL routing setup
3. `backend/src/config/asgi.py` — ASGI entry point for the async server
4. `backend/src/api/api.py` — Main API instance creation, router registration
5. `backend/src/api/schemas/expert.py` — Pydantic schemas defining the shape of request/response data for the expert system
6. `backend/src/api/routers/expert.py` — Expert system API endpoints (`/diagnose`, `/symptoms`, `/diseases`)

**Why Django + Django Ninja**: Django provides a mature, battle-tested web framework with built-in security. Django Ninja adds modern API features (automatic validation, OpenAPI docs) with minimal boilerplate — it uses Python type hints instead of verbose serializer classes.

### Phase 4: AI/LLM Integration

**What happened**: A conversational AI layer was added, connecting to the Groq API (which hosts open-source LLM models like Llama 3.3). A RAG (Retrieval-Augmented Generation) system was built so the AI's responses are grounded in the curated medical knowledge from Phase 1.

**Files created (in order)**:

1. `backend/src/lib/ai/llm_client.py` — HTTP client that sends messages to Groq's API and receives AI responses
2. `backend/src/lib/ai/knowledge_base.py` — RAG system that loads the 25 medical Markdown files, indexes them by keyword, and retrieves relevant chunks when users ask questions
3. `backend/src/lib/ai/prompts.py` — System prompts that define the AI's role, behavior rules, medical guidelines, and safety disclaimers
4. `backend/src/api/schemas/chat.py` — Pydantic schemas for chat request/response data
5. `backend/src/api/routers/chat.py` — Chat API endpoints (`/message`, `/models`)

**Why RAG instead of just using the LLM directly**: LLMs have general knowledge but may not be specialized in tropical medicine. By retrieving relevant medical text from our own curated files and injecting it into the prompt, we ensure the AI's responses are grounded in verified medical information rather than relying solely on its training data.

**Why Groq**: Groq provides extremely fast inference for open-source models (Llama 3.3 70B). It uses an OpenAI-compatible API format, which means switching to OpenAI, Anthropic, or any other provider in the future would require minimal code changes.

### Phase 5: Frontend Development

**What happened**: A modern web interface was built using Next.js (React) with TypeScript. The frontend communicates with the backend API and presents two user-facing modes: Chat and Expert.

**Files created (in order)**:

1. `frontend/lib/api/types/mesa.types.ts` — TypeScript type definitions matching the backend schemas
2. `frontend/lib/api/ApiClient.ts` — HTTP client for making API calls to the backend
3. `frontend/lib/api/BackendRoutes.ts` — Constants for all backend API URLs
4. `frontend/lib/api/services/MesaService.ts` — Service layer wrapping API calls with MESA-specific methods
5. `frontend/lib/api/stores/mesaStore.ts` — Zustand state management (335 lines tracking all app state)
6. `frontend/app/layout.tsx` — Root layout (HTML structure, fonts, metadata)
7. `frontend/app/mesa/page.tsx` — Main page that loads data and renders the interface
8. `frontend/components/mesa/MesaHeader.tsx` — Header with mode switching
9. `frontend/components/mesa/MesaChat.tsx` — Chat interface (message bubbles, markdown rendering)
10. `frontend/components/mesa/MesaExpert.tsx` — Expert system interface (symptom forms, results)
11. `frontend/components/mesa/MesaVoiceOverlay.tsx` — Voice mode overlay (placeholder)

**Why Next.js + TypeScript**: Next.js is the industry standard for React apps — it provides server-side rendering, optimized builds, and file-based routing out of the box. TypeScript adds type safety, which catches bugs early and makes the code self-documenting (important for a team project).

**Why Zustand for state management**: Simpler than Redux (no boilerplate), but powerful enough to manage complex state (chat history, selected symptoms, diagnosis results, model selection) across multiple components.

### Phase 6: Containerization & Deployment

**What happened**: Docker containers were created for both frontend and backend, and a docker-compose file was written to run them together. The app was deployed to Render (backend) and Vercel (frontend).

**Files created**:

1. `backend/Dockerfile` — Builds the Python backend image (based on Python 3.8-slim)
2. `frontend/Dockerfile` — Multi-stage build for the Next.js frontend (Node 20 Alpine)
3. `docker-compose.yml` — Orchestrates both containers together
4. `Makefile` (root) — Shortcut commands for Docker operations
5. `backend/Makefile` and `frontend/Makefile` — Service-specific shortcut commands

**Why Docker**: Ensures the app runs identically everywhere — on any developer's laptop, on a test server, or in the cloud. Eliminates "it works on my machine" problems.

### The Role of AI in Development

AI coding assistants were used as a development aid during this project, primarily for:

- **Scaffolding boilerplate code** — generating repetitive setup code (Django config, API schemas, TypeScript types)
- **Writing diagnostic rules** — translating medical knowledge from Markdown files into Experta rule syntax
- **Frontend components** — generating React component structures and Tailwind CSS styling
- **Documentation** — helping structure API documentation and code comments

The core architectural decisions, medical knowledge curation, and system design were done by the development team. AI assisted with implementation speed, not with design decisions.

### Development Summary Diagram

```text
Phase 1          Phase 2           Phase 3          Phase 4          Phase 5           Phase 6
Research    -->  Expert System -->  Backend API -->  AI/LLM Layer --> Frontend      --> Deployment

25 medical       facts.py          settings.py      llm_client.py    types &          Dockerfiles
Markdown         diagnosis_        urls.py          knowledge_       ApiClient        docker-compose
files            engine.py         api.py           base.py          mesaStore        Render +
                 main.py           schemas/         prompts.py       Components       Vercel
                                   routers/         chat router      Pages
```

---

## 4. How It Works (Non-Technical)

```
┌─────────────────────────────────────────────────┐
│                  THE USER                        │
│    (Healthcare worker or medical student)        │
└────────────────────┬────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
    ┌─────▼─────┐        ┌─────▼─────┐
    │  EXPERT   │        │   CHAT    │
    │   MODE    │        │   MODE    │
    │           │        │           │
    │ Pick      │        │ Type:     │
    │ symptoms  │        │ "Patient  │
    │ from a    │        │  has high │
    │ checklist │        │  fever    │
    │           │        │  and..." │
    └─────┬─────┘        └─────┬─────┘
          │                     │
          │                     │
    ┌─────▼──────────────┐ ┌───▼─────────────────┐
    │  RULE ENGINE       │ │  AI MODEL           │
    │                    │ │                      │
    │  100+ medical      │ │  Llama 3.3 (via     │
    │  rules check       │ │  Groq) reads medical│
    │  symptoms against  │ │  knowledge files    │
    │  known disease     │ │  and responds        │
    │  patterns          │ │  conversationally   │
    └─────┬──────────────┘ └───┬─────────────────┘
          │                     │
          └──────────┬──────────┘
                     │
         ┌───────────▼───────────┐
         │      RESULTS          │
         │                       │
         │  - Possible diseases  │
         │  - Confidence level   │
         │  - Treatment advice   │
         │  - Danger signs       │
         │  - "See a doctor" ⚠️  │
         └───────────────────────┘
```

---

## 5. Technology Stack & Why Each Was Chosen

### Backend (The Server / Brain)

| Technology | What It Is | Why It Was Chosen |
|-----------|-----------|-------------------|
| **Python 3.8** | Programming language | Required for compatibility with Experta (the rule engine library). Python is also the most popular language for AI/ML projects. |
| **Django 4.2** | Web framework | Industry-standard Python web framework. Provides project structure, security features (CSRF protection, CORS), and a built-in admin system. |
| **Django Ninja** | API framework (sits on top of Django) | Modern, fast alternative to Django REST Framework. Uses Python type hints for automatic validation and generates Swagger/OpenAPI docs automatically. |
| **Experta 1.9.4** | Rule-based expert system engine | Python implementation of CLIPS (a NASA-developed expert system language). Allows writing medical diagnostic rules as IF-THEN statements with priority levels. |
| **Groq API** | AI model provider | Provides extremely fast inference (responses) for open-source LLM models like Llama 3.3. Uses an OpenAI-compatible API, making it easy to switch providers later. |
| **httpx** | HTTP client | Modern async HTTP library for making API calls to Groq. Supports both sync and async operations. |
| **Uvicorn** | ASGI server | High-performance async server that runs the Django app. Supports hot-reloading during development. |
| **python-dotenv** | Environment config | Loads sensitive configuration (API keys) from `.env` files so secrets aren't hardcoded in code. |

### Frontend (What Users See & Interact With)

| Technology | What It Is | Why It Was Chosen |
|-----------|-----------|-------------------|
| **Next.js 16** | React framework | Provides server-side rendering, file-based routing, and optimized builds. Industry standard for modern React apps. |
| **React 19** | UI library | The most popular JavaScript library for building user interfaces. Component-based architecture makes the code modular and reusable. |
| **TypeScript** | Typed JavaScript | Adds type safety to JavaScript — catches errors at compile time rather than runtime. Makes the codebase more reliable and self-documenting. |
| **Zustand** | State management | Lightweight alternative to Redux. Manages app state (selected symptoms, chat history, diagnoses) with minimal boilerplate code. |
| **Tailwind CSS** | Styling framework | Utility-first CSS framework. Allows rapid UI development by applying styles directly in HTML/JSX. Produces small CSS bundles in production. |
| **react-markdown** | Markdown renderer | Renders the AI's responses (which come in Markdown format) as properly formatted HTML with headings, lists, bold text, etc. |
| **pnpm** | Package manager | Faster and more disk-efficient than npm. Uses hard links to save space when multiple projects share dependencies. |

### Infrastructure

| Technology | What It Is | Why It Was Chosen |
|-----------|-----------|-------------------|
| **Docker** | Containerization | Packages the app with all its dependencies so it runs the same everywhere — your laptop, a server, the cloud. |
| **Docker Compose** | Multi-container orchestration | Runs both frontend and backend together with a single command (`docker-compose up`). |
| **SQLite** | Database (development) | Simple file-based database. Used for development — would be replaced with PostgreSQL in production. |
| **Render.com** | Backend hosting | Cloud platform for deploying the backend API. |
| **Vercel** | Frontend hosting | Optimized platform for Next.js deployments. Provides CDN, automatic HTTPS, and preview deployments. |

---

## 6. Project Structure (File-by-File Walkthrough)

### Root Level

```
501_ai_health_system/
│
├── docker-compose.yml    ← Defines how to run both frontend + backend together in Docker
├── Makefile              ← Shortcut commands (e.g., `make up` to start everything)
├── README.md             ← Project overview and setup instructions
├── LICENSE               ← Open source license
├── .gitignore            ← Tells Git which files to ignore (node_modules, .env, etc.)
│
├── backend/              ← The server (Python/Django) — handles logic and AI
└── frontend/             ← The website (Next.js/React) — what users see
```

### Backend Structure

```
backend/
│
├── .env.example          ← Template showing what environment variables are needed
├── requirements.txt      ← List of Python packages the project depends on
├── Dockerfile            ← Instructions for building the backend Docker image
├── Makefile              ← Backend-specific shortcut commands
├── manage.py             ← Django's command-line utility (run server, migrations, etc.)
│
└── src/                  ← All source code lives here
    │
    ├── config/           ← PROJECT CONFIGURATION
    │   ├── settings.py   ← Django settings: database, security, CORS, installed apps
    │   ├── urls.py       ← URL routing: maps /api/* to the API layer
    │   ├── asgi.py       ← Entry point for the async server (Uvicorn)
    │   └── wsgi.py       ← Entry point for traditional server (not used in development)
    │
    ├── api/              ← API LAYER (handles HTTP requests/responses)
    │   ├── api.py        ← Main API setup: creates the API instance, registers routers
    │   │
    │   ├── routers/      ← ENDPOINT HANDLERS (where requests are processed)
    │   │   ├── expert.py ← Expert system endpoints: /diagnose, /symptoms, /diseases
    │   │   └── chat.py   ← Chat endpoints: /message, /models
    │   │
    │   └── schemas/      ← DATA SHAPES (defines what data looks like going in/out)
    │       ├── expert.py ← Defines: SymptomInput, PatientInput, DiagnoseRequest, etc.
    │       └── chat.py   ← Defines: ChatMessage, ChatRequest, ChatResponse, etc.
    │
    └── lib/              ← CORE BUSINESS LOGIC (the "brains")
        │
        ├── expert_system/          ← THE RULE ENGINE
        │   ├── diagnosis_engine.py ← THE MAIN FILE: 650+ lines of medical rules
        │   │                          (IF patient has X + Y symptoms THEN suspect Z disease)
        │   ├── facts.py            ← Defines "facts" the engine reasons about
        │   │                          (Symptom, Patient, LabResult, etc.)
        │   ├── main.py             ← CLI interface to test the expert system directly
        │   ├── visualize_knowledge.py ← Visualizes the knowledge base structure
        │   │
        │   └── raw_knowledge/      ← MEDICAL REFERENCE DATA (Markdown files)
        │       ├── cholera/        ← 5 files covering cholera comprehensively
        │       │   ├── cholera1.md ... cholera5.md
        │       ├── malaria/        ← 11 files covering malaria comprehensively
        │       │   ├── malaria1.md ... malaria11.md
        │       └── typhoid_fever/  ← 9 files covering typhoid comprehensively
        │           ├── typhoid_fever1.md ... typhoid_fever9.md
        │
        └── ai/                     ← THE AI/LLM LAYER
            ├── llm_client.py       ← Connects to Groq API, sends messages, gets responses
            │                          Supports multiple models (Llama, Mixtral, Gemma)
            ├── knowledge_base.py   ← RAG system: loads medical files, indexes them,
            │                          retrieves relevant info when user asks questions
            └── prompts.py          ← System prompts that tell the AI how to behave
                                       (role, guidelines, medical rules, safety disclaimers)
```

### Frontend Structure

```
frontend/
│
├── package.json          ← Lists JavaScript dependencies and scripts
├── tsconfig.json         ← TypeScript compiler configuration
├── Dockerfile            ← Instructions for building the frontend Docker image
├── Makefile              ← Frontend-specific shortcut commands
│
├── app/                  ← PAGES (Next.js App Router)
│   ├── layout.tsx        ← Root layout: wraps every page (HTML head, fonts, metadata)
│   ├── page.tsx          ← Home page: automatically redirects users to /mesa
│   ├── globals.css       ← Global CSS styles (Tailwind imports, custom styles)
│   │
│   └── mesa/
│       └── page.tsx      ← THE MAIN PAGE: renders the MESA interface
│                            Loads data (symptoms, diseases, models) on mount
│                            Switches between Chat, Expert, and Voice modes
│
├── components/           ← REUSABLE UI PIECES
│   └── mesa/
│       ├── index.ts              ← Exports all MESA components from one place
│       ├── MesaHeader.tsx        ← Top bar: mode switcher (Chat/Expert/Voice), settings
│       ├── MesaChat.tsx          ← Chat interface: message bubbles, input box, send button
│       │                            Handles markdown rendering, copy/edit/regenerate
│       ├── MesaExpert.tsx        ← Expert interface: symptom checkboxes, patient info form,
│       │                            lab results form, dehydration assessment, results display
│       └── MesaVoiceOverlay.tsx  ← Voice mode UI overlay (framework in place)
│
└── lib/                  ← UTILITIES & API INTEGRATION
    ├── utils.ts          ← Helper functions (classname merging, etc.)
    │
    └── api/
        ├── ApiClient.ts          ← HTTP client: handles all fetch requests to backend
        │                            Base URL, error handling, JSON parsing
        ├── BackendRoutes.ts      ← Constants: all backend API URLs in one place
        ├── FrontendRoutes.ts     ← Constants: all frontend page URLs in one place
        │
        ├── types/                ← TYPE DEFINITIONS
        │   ├── common.types.ts   ← Shared types (API responses, errors)
        │   └── mesa.types.ts     ← MESA-specific types (symptoms, diagnoses, chat messages)
        │
        ├── services/
        │   └── MesaService.ts    ← API service: wraps ApiClient with MESA-specific methods
        │                            (sendChatMessage, runDiagnosis, getSymptoms, etc.)
        │
        ├── stores/
        │   └── mesaStore.ts      ← STATE MANAGEMENT (Zustand store, 335 lines)
        │                            Tracks: mode, chat history, selected symptoms,
        │                            patient info, diagnosis results, available models
        │
        └── auth/
            └── TokenManager.ts   ← Token management (placeholder for future auth)
```

---

## 7. The Two Brains: Expert System vs AI Chat

This project uses a **hybrid approach** — two completely different methods of diagnosis that complement each other:

### Brain 1: Expert System (Rule-Based)

**How it thinks**: Like a medical textbook turned into code. It follows strict IF-THEN rules.

```
IF patient has "rice-water stool" AND "severe dehydration"
THEN diagnose: Cholera (confidence: CONFIDENT)
     urgency: HIGH
     treatment: Start IV fluids immediately
```

**Strengths**:
- Predictable and explainable — you can trace exactly WHY it gave a diagnosis
- Follows WHO protocols exactly
- Never "hallucinates" or makes things up
- Perfect for structured clinical assessments

**Weaknesses**:
- Can only handle symptoms it was programmed for
- No natural language understanding
- Rigid — can't handle "my stomach hurts" (needs specific symptom selections)

**File**: `backend/src/lib/expert_system/diagnosis_engine.py`

### Brain 2: AI Chat (LLM-Powered)

**How it thinks**: Like a knowledgeable medical assistant who can understand plain English and have a conversation.

```
User: "My patient has been having a high fever that goes up and down
       for about a week, and they seem confused"

AI: "The stepladder fever pattern you're describing, combined with
     altered mental status, raises concern for typhoid fever. I'd
     recommend checking for: 1) Rose spots on abdomen, 2) Relative
     bradycardia, 3) Blood culture..."
```

**Strengths**:
- Understands natural language
- Can ask follow-up questions
- Can explain reasoning in plain English
- Flexible — handles varied descriptions of symptoms

**Weaknesses**:
- May occasionally give imperfect responses (LLM limitation)
- Less traceable than rule-based reasoning
- Depends on external API (Groq) — needs internet connection

**Files**: `backend/src/lib/ai/llm_client.py`, `knowledge_base.py`, `prompts.py`

### Why Use Both?

| Scenario | Best Mode |
|----------|-----------|
| Structured clinical assessment with known symptoms | Expert Mode |
| Patient describing symptoms in their own words | Chat Mode |
| Need an auditable, rule-based diagnosis | Expert Mode |
| Need to explore differential diagnoses through conversation | Chat Mode |
| Following WHO dehydration protocol | Expert Mode |
| Explaining a diagnosis to a patient or student | Chat Mode |

---

## 8. How Data Flows Through the System

### Expert Mode Flow (Step by Step)

```
Step 1: User opens MESA → frontend loads at /mesa
        File: frontend/app/mesa/page.tsx

Step 2: User switches to Expert Mode
        File: frontend/components/mesa/MesaHeader.tsx (mode switcher)
        State: mesaStore.ts → setMode('expert')

Step 3: Frontend fetches available symptoms and diseases from backend
        File: frontend/lib/api/services/MesaService.ts → getSymptoms()
        API:  GET /api/expert/symptoms
        File: backend/src/api/routers/expert.py → get_symptoms()

Step 4: User selects symptoms (e.g., fever, diarrhea, vomiting)
        File: frontend/components/mesa/MesaExpert.tsx
        State: mesaStore.ts → toggleSymptom()

Step 5: User fills optional patient info (age, travel history)
        File: frontend/components/mesa/MesaExpert.tsx
        State: mesaStore.ts → setPatientInfo()

Step 6: User clicks "Run Diagnosis"
        File: frontend/components/mesa/MesaExpert.tsx → handleDiagnose()
        State: mesaStore.ts → runExpertDiagnosis()
        API:  POST /api/expert/diagnose (sends all selected data)

Step 7: Backend receives the request
        File: backend/src/api/routers/expert.py → diagnose()
        Validates data using: backend/src/api/schemas/expert.py

Step 8: Backend creates the expert system engine and feeds it facts
        File: backend/src/lib/expert_system/diagnosis_engine.py
        - Creates a DiagnosisEngine instance
        - Converts symptoms → Fact objects (from facts.py)
        - Runs the engine → applies 100+ rules
        - Rules fire based on symptom combinations

Step 9: Engine produces results
        - Diagnoses with confidence levels (confirmed/confident/suspect/uncertain)
        - Treatment recommendations
        - Danger sign flags
        - WHO dehydration classification (Plan A/B/C)

Step 10: Results sent back to frontend and displayed
         File: frontend/components/mesa/MesaExpert.tsx → diagnosis results section
         State: mesaStore.ts → diagnosisResult
```

### Chat Mode Flow (Step by Step)

```
Step 1: User opens MESA → frontend loads at /mesa
        File: frontend/app/mesa/page.tsx

Step 2: User stays in Chat Mode (default)
        File: frontend/components/mesa/MesaChat.tsx

Step 3: User types a message: "My patient has high fever and headache"
        State: mesaStore.ts → conversationHistory

Step 4: Message sent to backend
        File: frontend/lib/api/services/MesaService.ts → sendChatMessage()
        API:  POST /api/chat/message
        Sends: { message, conversation_history, model }

Step 5: Backend receives the message
        File: backend/src/api/routers/chat.py → send_message()
        Validates using: backend/src/api/schemas/chat.py

Step 6: Backend extracts medical keywords from user message
        File: backend/src/api/routers/chat.py
        - Scans for symptom keywords (fever, headache, diarrhea, etc.)
        - Scans for disease mentions (malaria, typhoid, cholera)

Step 7: Knowledge Base retrieves relevant medical information
        File: backend/src/lib/ai/knowledge_base.py
        - Looks up extracted symptoms/diseases in indexed knowledge files
        - Returns relevant medical text chunks from raw_knowledge/ files
        - Acts as a RAG (Retrieval-Augmented Generation) system

Step 8: System prompt is built
        File: backend/src/lib/ai/prompts.py
        - Base prompt: defines the AI's role and behavior rules
        - Expert rules: embeds diagnostic rules from the expert system
        - Knowledge context: adds retrieved medical information
        - Safety guidelines: reminds AI to recommend professional consultation

Step 9: Message sent to Groq API (external AI service)
        File: backend/src/lib/ai/llm_client.py
        - Sends: system prompt + conversation history + user message
        - Model: Llama 3.3 70B (default) or user-selected model
        - Receives: AI-generated response

Step 10: Response sent back to frontend
         API Response: { response, model_used, extracted_symptoms, suggested_diseases }
         File: frontend/components/mesa/MesaChat.tsx → displays message bubble
         State: mesaStore.ts → conversationHistory updated
```

---

## 9. The Expert System (Rule Engine) Explained

### What Is an Expert System?

An expert system is software that mimics the decision-making of a human expert. It uses a **knowledge base** (facts) and an **inference engine** (rules) to reach conclusions.

**Real-world analogy**: Imagine a doctor's brain distilled into IF-THEN rules:
- IF patient has rice-water stool → suspect cholera
- IF patient has cyclical fever every 48 hours → suspect malaria
- IF blood culture is positive for S. typhi → confirm typhoid

### How the Rule Engine Works

**File**: `backend/src/lib/expert_system/diagnosis_engine.py` (653 lines)

The engine uses **Experta**, a Python library based on CLIPS (originally developed by NASA for expert systems).

#### Key Concepts:

1. **Facts** — Things we know about the patient
   - `Symptom(name="fever", severity="high", duration_days=7)`
   - `Patient(age=25, recent_travel="endemic_area")`
   - `LabResult(test_name="blood_culture", result="positive")`

2. **Rules** — IF-THEN logic with priorities
   ```
   @Rule(Symptom(name="rice_water_stool"), salience=90)  ← high priority
   def cholera_pathognomonic(self):
       self.declare(Diagnosis(disease="cholera", confidence="confident"))
   ```

3. **Salience** — Priority of rules (higher = fires first)
   - 95-100: Laboratory confirmations (most reliable)
   - 85-90: Pathognomonic signs (classic disease indicators)
   - 70-80: Strong clinical presentations
   - 50-60: General suspicion rules

4. **Confidence Levels** — How sure the system is
   - `confirmed`: Lab test proves it (e.g., positive blood culture)
   - `confident`: Classic signs present (e.g., rice-water stool for cholera)
   - `suspect`: Clinical suspicion (e.g., fever + travel to endemic area)
   - `uncertain`: Not enough evidence

### Disease Rules Overview

#### Cholera Rules
| Rule | Trigger | Confidence |
|------|---------|-----------|
| Rice-water stool detected | `rice_water_stool` symptom | confident |
| Lab confirmation | Stool culture positive for V. cholerae | confirmed |
| Clinical combination | Profuse diarrhea + vomiting + dehydration | suspect |
| Rapid test positive | Cholera RDT positive | confirmed |

#### Malaria Rules
| Rule | Trigger | Confidence |
|------|---------|-----------|
| Malarial paroxysm | Cyclical fever + chills + sweating | confident |
| Lab confirmation | Blood smear positive for Plasmodium | confirmed |
| Severe malaria | Cerebral symptoms or blackwater fever | confident + HIGH URGENCY |
| Clinical suspicion | Fever + headache + endemic area travel | suspect |

#### Typhoid Rules
| Rule | Trigger | Confidence |
|------|---------|-----------|
| Stepladder fever + bradycardia | Classic presentation | confident |
| Lab confirmation | Blood culture positive for S. typhi | confirmed |
| Widal test positive | Titer ≥ 1:160 | confirmed |
| Rose spots + prolonged fever | Clinical signs | suspect |

### WHO Dehydration Classification

The system also classifies dehydration severity using WHO standards:

| Classification | Signs | Treatment Plan |
|---------------|-------|----------------|
| **Plan A** (No dehydration) | Alert, drinks normally, normal skin pinch | Home treatment, oral fluids |
| **Plan B** (Some dehydration) | Restless, drinks eagerly, slow skin pinch | ORS (Oral Rehydration Salts) under supervision |
| **Plan C** (Severe dehydration) | Lethargic/unconscious, sunken eyes, very slow skin pinch | Emergency IV fluids |

---

## 10. The AI Chat System Explained

### Architecture: RAG (Retrieval-Augmented Generation)

The chat system uses a technique called **RAG** — it doesn't rely solely on the AI model's built-in knowledge. Instead, it **retrieves** relevant medical information from local files and **injects** it into the prompt before the AI generates a response.

**Why RAG?**
- The AI model may not have specialized tropical medicine knowledge
- RAG ensures responses are grounded in curated medical data
- Makes the system more accurate and less prone to hallucination

### Components:

#### 1. LLM Client (`backend/src/lib/ai/llm_client.py`)

Connects to the **Groq API** (a fast AI inference provider):

- **Default Model**: Llama 3.3 70B — a powerful open-source model with 70 billion parameters
- **API Format**: OpenAI-compatible (same request/response format as ChatGPT's API)
- **Other Available Models**:
  - Llama 3.1 8B — faster, less capable (for quick responses)
  - Mixtral 8x7B — mixture-of-experts architecture
  - Gemma 2 9B — Google's efficient model

#### 2. Knowledge Base (`backend/src/lib/ai/knowledge_base.py`)

The RAG retrieval system:

- **Loads** 25 medical markdown files on startup
- **Indexes** them by keywords (symptoms, diseases, treatment terms)
- **Chunks** files by markdown headers (sections)
- **Retrieves** the most relevant 3-5 chunks based on the user's message
- **Scoring**: Simple keyword overlap — counts how many relevant terms appear in each chunk

#### 3. System Prompts (`backend/src/lib/ai/prompts.py`)

Tells the AI how to behave:

- **Role**: "You are a Medical Diagnostic Assistant specializing in tropical diseases"
- **Capabilities**: Cholera, malaria, typhoid analysis
- **Safety Rules**: Never give definitive diagnoses, always recommend professional evaluation
- **Danger Signs**: 8 critical symptoms that require immediate medical attention
- **Conversation Style**: Ask about symptoms systematically, assess severity, provide structured assessments

---

## 11. The Frontend (What Users See)

### Page Structure

The app has essentially **one main page** (`/mesa`) with three modes:

#### MesaHeader (`components/mesa/MesaHeader.tsx`)
- Mode switcher buttons: Chat | Expert | Voice
- Settings access (model selection, etc.)

#### MesaChat (`components/mesa/MesaChat.tsx`)
- Message bubble interface (like WhatsApp/iMessage)
- User messages on the right, AI responses on the left
- AI responses rendered as Markdown (headings, lists, bold, etc.)
- Features: copy message, edit message, regenerate response
- Model selector (choose which AI model to use)

#### MesaExpert (`components/mesa/MesaExpert.tsx`)
- Multi-step form interface:
  1. **Symptom Selection** — checkboxes for all supported symptoms
  2. **Patient Information** — age, sex, travel history
  3. **Lab Results** — test name and result (optional)
  4. **Dehydration Assessment** — WHO dehydration signs (optional)
  5. **Results Display** — diagnoses with confidence, treatments, danger signs

#### MesaVoiceOverlay (`components/mesa/MesaVoiceOverlay.tsx`)
- Voice interaction interface (framework/placeholder — not fully implemented)

### State Management (`lib/api/stores/mesaStore.ts`)

Uses **Zustand** (a lightweight state management library):

```
What the store tracks:
├── Current mode (chat / expert / voice)
├── Chat state:
│   ├── All messages in the conversation
│   ├── Which AI model is selected
│   ├── Symptoms extracted from chat
│   └── Diseases the AI suggested
├── Expert state:
│   ├── Which symptoms are checked
│   ├── Patient demographics
│   ├── Lab results entered
│   ├── Dehydration signs selected
│   └── Diagnosis results
└── Metadata:
    ├── List of all available symptoms
    ├── List of all supported diseases
    └── List of available AI models
```

---

## 12. API Endpoints (How Frontend Talks to Backend)

All API endpoints start with `/api/` and are defined in the backend.

### General

| Method | URL | What It Does |
|--------|-----|-------------|
| `GET` | `/api/` | Returns API info (name, version, status) |
| `GET` | `/api/ping` | Health check — returns "pong" if server is running |
| `GET` | `/api/docs` | Opens interactive Swagger documentation |

### Expert System Endpoints

| Method | URL | What It Does | Input | Output |
|--------|-----|-------------|-------|--------|
| `POST` | `/api/expert/diagnose` | Runs a full diagnosis | Symptoms, patient info, lab results, dehydration signs | Diagnoses with confidence levels, treatments, danger signs |
| `GET` | `/api/expert/symptoms` | Lists all symptoms the system knows about | None | Array of symptom names and categories |
| `GET` | `/api/expert/diseases` | Lists all supported diseases | None | Array of disease names and descriptions |
| `GET` | `/api/expert/diseases/{name}` | Details about a specific disease | Disease name in URL | Disease info, common symptoms, diagnostic criteria |

### AI Chat Endpoints

| Method | URL | What It Does | Input | Output |
|--------|-----|-------------|-------|--------|
| `POST` | `/api/chat/message` | Sends a message to the AI | Message text, conversation history, model choice | AI response, extracted symptoms, suggested diseases |
| `GET` | `/api/chat/models` | Lists available AI models | None | Array of model IDs and descriptions |
| `POST` | `/api/chat/validate-model` | Checks if a model ID is valid | Model ID | Valid/invalid status |

---

## 13. The Knowledge Base (Medical Data)

### Where the Medical Knowledge Lives

```
backend/src/lib/expert_system/raw_knowledge/
│
├── cholera/              (5 files)
│   ├── cholera1.md       - Overview, epidemiology, transmission
│   ├── cholera2.md       - Clinical features, pathophysiology
│   ├── cholera3.md       - Diagnosis methods
│   ├── cholera4.md       - Treatment protocols
│   └── cholera5.md       - Prevention, vaccines
│
├── malaria/              (11 files)
│   ├── malaria1.md       - Overview, Plasmodium species
│   ├── malaria2.md       - Transmission, mosquito lifecycle
│   ├── malaria3.md       - Clinical manifestations
│   ├── malaria4.md       - Severe/complicated malaria
│   ├── malaria5.md       - Diagnosis (blood smear, RDT)
│   ├── malaria6.md       - Treatment (ACTs, chloroquine)
│   ├── malaria7.md       - Drug resistance
│   ├── malaria8.md       - Prevention (bed nets, prophylaxis)
│   ├── malaria9.md       - Malaria in pregnancy
│   ├── malaria10.md      - Epidemiology and control
│   └── malari11.md       - Special populations
│
└── typhoid_fever/        (9 files)
    ├── typhoid_fever1.md  - Overview, S. typhi bacteriology
    ├── typhoid_fever2.md  - Epidemiology, transmission
    ├── typhoid_fever3.md  - Clinical stages (week by week)
    ├── typhoid_fever4.md  - Complications (perforation, bleeding)
    ├── typhoid_fever5.md  - Diagnosis (cultures, Widal, Typhidot)
    ├── typhoid_fever6.md  - Treatment (antibiotics)
    ├── typhoid_fever7.md  - Drug resistance
    ├── typhoid_fever8.md  - Prevention and vaccines
    └── typhoid_fever9.md  - Carrier state management
```

### How Knowledge Is Used

1. **Expert System**: The rules in `diagnosis_engine.py` are **derived from** this knowledge but are coded as explicit IF-THEN rules.
2. **AI Chat**: The `knowledge_base.py` **loads these files at startup**, indexes them by keyword, and retrieves relevant chunks when the user asks questions. This is the RAG (Retrieval-Augmented Generation) component.

---

## 14. Deployment & Infrastructure

### Development Setup

```bash
# Terminal 1: Start the backend
cd backend
python -m venv .venv          # Create a Python virtual environment
source .venv/bin/activate      # Activate it
pip install -r requirements.txt # Install dependencies
cp .env.example .env           # Create .env file
# Edit .env to add your GROQ_API_KEY
make dev                       # Starts backend at http://localhost:8000

# Terminal 2: Start the frontend
cd frontend
pnpm install                   # Install dependencies
cp .env.example .env.local     # Create .env file
pnpm dev                       # Starts frontend at http://localhost:3000
```

### Docker Setup

```bash
# From root directory — starts everything
docker-compose up --build      # or: make up
```

The `docker-compose.yml` defines two services:
- **backend**: Python 3.8 container running Django/Uvicorn on port 8000
- **frontend**: Node 20 Alpine container running Next.js on port 3000

### Production Deployment

| Component | Platform | URL |
|-----------|----------|-----|
| Backend API | Render.com | `https://sen-grp-1-backend.onrender.com` |
| Frontend | Vercel | `https://sen-grp-1-frontend.vercel.app` |

---

## 15. Security & Ethical Considerations

### Security Measures In Place

- **CORS Protection**: Only whitelisted origins (the frontend) can call the API
- **CSRF Protection**: Django's built-in cross-site request forgery protection
- **Environment Variables**: API keys stored in `.env` files, never in code
- **Input Validation**: All API inputs validated via Pydantic schemas

### Ethical Safeguards

- **Medical Disclaimer**: The system is for **educational/informational purposes only**
- **Always Recommends Professional Care**: Every response includes advice to consult a healthcare professional
- **Confidence Transparency**: Shows confidence levels so users know how certain the system is
- **Danger Sign Alerts**: Flags critical symptoms that require immediate medical attention
- **No Definitive Diagnoses**: System explicitly says it provides **suggestions**, not diagnoses

### What's Not Implemented (Would Need for Production)

- User authentication (login system)
- Rate limiting (prevent API abuse)
- Data encryption at rest
- Audit logging
- HIPAA compliance measures

---

## 16. Limitations & Future Work

### Current Limitations

1. **Only 3 diseases** — Cholera, Malaria, Typhoid (tropical regions have many more)
2. **No persistent storage** — Conversation history is lost when you refresh the page
3. **No user accounts** — No login, no saved patient records
4. **Basic RAG** — Uses keyword matching instead of semantic/vector search
5. **No streaming** — AI responses arrive all at once (not word-by-word like ChatGPT)
6. **Internet dependent** — Chat mode requires connection to Groq API
7. **English only** — No multi-language support

### Planned Improvements

- Add more diseases (Dengue, Typhus, Yellow Fever, etc.)
- Implement conversation persistence (save chats to database)
- Add user authentication and role-based access
- Upgrade RAG to use vector embeddings (sentence-transformers) for better retrieval
- Add streaming responses for the chat
- Build an admin dashboard for managing the knowledge base
- Add multi-language support for local healthcare workers
- Implement rate limiting and production monitoring

---

## Quick Reference: Key Files to Know

| If asked about... | Look at this file |
|---|---|
| How the project is configured | `backend/src/config/settings.py` |
| How API routes are set up | `backend/src/config/urls.py` → `backend/src/api/api.py` |
| How the expert system diagnoses | `backend/src/lib/expert_system/diagnosis_engine.py` |
| What facts/data the expert system uses | `backend/src/lib/expert_system/facts.py` |
| How the AI chat works | `backend/src/lib/ai/llm_client.py` |
| How medical knowledge is retrieved | `backend/src/lib/ai/knowledge_base.py` |
| What the AI is told to do | `backend/src/lib/ai/prompts.py` |
| How the frontend is structured | `frontend/app/mesa/page.tsx` |
| How state is managed | `frontend/lib/api/stores/mesaStore.ts` |
| How the frontend calls the backend | `frontend/lib/api/services/MesaService.ts` |
| What data shapes look like | `frontend/lib/api/types/mesa.types.ts` |
| The medical knowledge itself | `backend/src/lib/expert_system/raw_knowledge/` |

---

*This project demonstrates a hybrid AI architecture combining deterministic rule-based reasoning with modern LLM capabilities, applied to a real-world healthcare problem in tropical medicine.*
