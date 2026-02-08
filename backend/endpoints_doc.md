# API Endpoints Documentation

Complete API reference for frontend integration with the Medical Expert System.

**Base URL:** `http://localhost:8000/api`  
**Documentation UI:** `http://localhost:8000/api/docs` (Swagger)

---

## Table of Contents

1. [General Endpoints](#general-endpoints)
2. [Expert System Endpoints](#expert-system-endpoints)
3. [AI Chat Endpoints](#ai-chat-endpoints)
4. [Data Types Reference](#data-types-reference)
5. [Error Handling](#error-handling)
6. [Integration Examples](#integration-examples)

---

## General Endpoints

### GET `/api/`
Returns API information and status.

**Response:**
```json
{
  "name": "Medical Expert API",
  "version": "1.0.0",
  "status": "operational",
  "docs": "/api/docs",
  "endpoints": {
    "expert": "/api/expert - Structured expert system access",
    "chat": "/api/chat - AI-powered conversational assistant"
  }
}
```

### GET `/api/ping`
Health check endpoint.

**Response:**
```json
{
  "message": "pong"
}
```

---

## Expert System Endpoints

The expert system provides deterministic, rule-based diagnosis using structured symptom input.

### POST `/api/expert/diagnose`

Run the expert system diagnosis on provided symptoms.

**Request Body:**
```json
{
  "symptoms": [
    {
      "name": "fever",
      "present": true,
      "pattern": "cyclical",
      "severity": "moderate",
      "duration_days": 3
    },
    {
      "name": "chills",
      "present": true
    },
    {
      "name": "sweating",
      "present": true
    }
  ],
  "patient": {
    "age": 28,
    "travel_endemic_area": true,
    "unsafe_water": false
  },
  "lab_results": [
    {
      "test": "rdt_malaria",
      "result": "positive"
    }
  ],
  "dehydration_signs": [
    {
      "sign": "mental_state",
      "finding": "alert"
    },
    {
      "sign": "skin_pinch",
      "finding": "normal"
    }
  ]
}
```

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `symptoms` | array | ✅ Yes | List of symptoms (min 1) |
| `patient` | object | No | Patient demographics and exposure history |
| `lab_results` | array | No | Laboratory test results |
| `dehydration_signs` | array | No | WHO dehydration assessment |

**Symptom Object:**

| Field | Type | Required | Values |
|-------|------|----------|--------|
| `name` | string | ✅ Yes | See [Valid Symptoms](#valid-symptoms) |
| `present` | boolean | No | Default: `true` |
| `severity` | string | No | `"mild"`, `"moderate"`, `"severe"` |
| `duration_days` | integer | No | Number of days |
| `pattern` | string | No | `"cyclical"`, `"stepladder"`, `"continuous"` |
| `description` | string | No | Additional details (e.g., `"rice_water"`) |

**Patient Object:**

| Field | Type | Description |
|-------|------|-------------|
| `age` | integer | Patient age in years |
| `is_child` | boolean | Under 18 years old |
| `is_pregnant` | boolean | Pregnancy status |
| `travel_endemic_area` | boolean | Recent travel to endemic area (30 days) |
| `endemic_resident` | boolean | Lives in endemic area |
| `unsafe_water` | boolean | Consumed untreated water |
| `street_food` | boolean | Consumed raw street food |
| `household_contact` | boolean | Contact with confirmed case |

**Lab Result Object:**

| Field | Type | Required | Values |
|-------|------|----------|--------|
| `test` | string | ✅ Yes | `"blood_smear"`, `"rdt_malaria"`, `"stool_culture"`, `"rdt_cholera"`, `"blood_culture"`, `"widal"`, `"typhidot"` |
| `result` | string | ✅ Yes | `"positive"`, `"negative"`, `"pending"` |
| `details` | string | No | Species, titer, etc. |

**Dehydration Sign Object:**

| Field | Type | Required | Values |
|-------|------|----------|--------|
| `sign` | string | ✅ Yes | `"mental_state"`, `"eyes"`, `"skin_pinch"`, `"thirst"` |
| `finding` | string | ✅ Yes | See [Dehydration Findings](#dehydration-findings) |

**Response:**
```json
{
  "diagnoses": [
    {
      "disease": "malaria",
      "confidence": "confident",
      "reason": "Classic malarial paroxysm: cyclical fever with chills followed by sweating",
      "severity": null,
      "recommendation": null
    }
  ],
  "recommendations": [],
  "dehydration_level": "none",
  "treatment_plan": "A",
  "disclaimer": "This is an expert system assessment, not a medical diagnosis. Please consult a healthcare professional for proper evaluation and treatment."
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `diagnoses` | array | List of possible diagnoses, sorted by confidence |
| `recommendations` | array | Urgent actions and general recommendations |
| `dehydration_level` | string | `"none"`, `"some"`, `"severe"` (if assessed) |
| `treatment_plan` | string | WHO plan `"A"`, `"B"`, or `"C"` (if assessed) |
| `disclaimer` | string | Medical disclaimer |

**Diagnosis Confidence Levels:**

| Level | Meaning | UI Representation |
|-------|---------|-------------------|
| `confirmed` | Laboratory-verified | 🟢 High confidence |
| `confident` | Pathognomonic signs present | 🟢 High confidence |
| `suspect` | Clinical suspicion | 🟡 Medium confidence |
| `uncertain` | Insufficient findings | 🔴 Low confidence |

---

### GET `/api/expert/symptoms`

Get list of all valid symptoms the expert system accepts.

**Response:**
```json
[
  {
    "name": "fever",
    "display_name": "Fever",
    "description": "Elevated body temperature",
    "options": {
      "pattern": ["cyclical", "stepladder", "continuous", "irregular"],
      "severity": ["mild", "moderate", "severe"]
    }
  },
  {
    "name": "chills",
    "display_name": "Chills/Rigors",
    "description": "Shaking or shivering episodes",
    "options": null
  }
  // ... more symptoms
]
```

**Use this endpoint to:**
- Build dynamic symptom selection forms
- Validate symptom names before submission
- Display available options for each symptom

---

### GET `/api/expert/diseases`

Get list of all diseases the expert system can diagnose.

**Response:**
```json
[
  {
    "name": "Cholera",
    "description": "Acute diarrheal infection caused by Vibrio cholerae bacteria, spread through contaminated water",
    "key_symptoms": ["diarrhea", "vomiting", "dehydration"],
    "pathognomonic_signs": ["Rice-water stool (pale, milky with mucus flecks)"]
  },
  {
    "name": "Malaria",
    "description": "Parasitic disease transmitted by infected Anopheles mosquitoes, caused by Plasmodium parasites",
    "key_symptoms": ["fever", "chills", "sweating", "headache", "body_aches"],
    "pathognomonic_signs": [
      "Classic malarial paroxysm (cyclical fever + chills + sweating)",
      "Bitter taste in mouth"
    ]
  },
  {
    "name": "Typhoid Fever",
    "description": "Enteric fever caused by Salmonella typhi bacteria, spread through contaminated food/water",
    "key_symptoms": ["fever", "headache", "abdominal_pain", "constipation"],
    "pathognomonic_signs": [
      "Stepladder fever pattern (gradually increasing)",
      "Relative bradycardia",
      "Rose spots on trunk"
    ]
  }
]
```

---

### GET `/api/expert/diseases/{disease_name}`

Get detailed information about a specific disease.

**Path Parameters:**
- `disease_name` - Disease name (case-insensitive, supports `_` or `-`)

**Example:** `GET /api/expert/diseases/malaria`

**Response:** Same as single disease object above.

**Error Response (404):**
```json
{
  "detail": "Disease 'unknown' not found. Available: ['cholera', 'malaria', 'typhoid_fever']"
}
```

---

## AI Chat Endpoints

The AI chat provides natural language interaction with diagnostic guidance.

### POST `/api/chat/message`

Send a message to the AI medical assistant.

**Request Body:**
```json
{
  "message": "I've been having fever and chills for the past 3 days. I recently traveled to Nigeria.",
  "conversation_history": [],
  "model": "llama-3.3-70b-versatile",
  "include_expert_context": true,
  "patient_context": {
    "age": 35,
    "travel_endemic_area": true
  }
}
```

**Request Fields:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `message` | string | ✅ Yes | - | User's message |
| `conversation_history` | array | No | `[]` | Previous messages for context |
| `model` | string | No | `"llama-3.3-70b-versatile"` | LLM model to use |
| `include_expert_context` | boolean | No | `true` | Include expert system rules in AI context |
| `patient_context` | object | No | `null` | Patient info for relevant responses |

**Conversation History Format:**
```json
[
  {"role": "user", "content": "I have a fever"},
  {"role": "assistant", "content": "I'm sorry to hear that..."}
]
```

**Response:**
```json
{
  "response": "I'm sorry to hear you're not feeling well. Based on your symptoms and recent travel to Nigeria (a malaria-endemic region), I'd like to ask a few more questions...",
  "model_used": "llama-3.3-70b-versatile",
  "conversation_history": [
    {"role": "user", "content": "I've been having fever and chills..."},
    {"role": "assistant", "content": "I'm sorry to hear you're not feeling well..."}
  ],
  "extracted_symptoms": ["fever", "chills"],
  "suggested_diseases": ["malaria"]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `response` | string | AI assistant's response |
| `model_used` | string | Model that generated the response |
| `conversation_history` | array | Updated history (include in next request) |
| `extracted_symptoms` | array | Symptoms extracted from conversation |
| `suggested_diseases` | array | Diseases suggested based on symptoms |

**Frontend Implementation Notes:**

1. **Maintain conversation state** - Store `conversation_history` from response and include it in the next request
2. **Handle extracted symptoms** - Display detected symptoms to user for confirmation
3. **Use suggested diseases** - Can be used to show relevant disease cards/info

---

### GET `/api/chat/models`

Get list of available LLM models.

**Response:**
```json
{
  "models": [
    {
      "id": "llama-3.3-70b-versatile",
      "name": "Llama 3.3 70B",
      "description": "Meta's latest Llama model, excellent for medical reasoning",
      "context_window": 128000
    },
    {
      "id": "llama-3.1-8b-instant",
      "name": "Llama 3.1 8B Instant",
      "description": "Fast, smaller Llama model for quick responses",
      "context_window": 128000
    },
    {
      "id": "mixtral-8x7b-32768",
      "name": "Mixtral 8x7B",
      "description": "Mistral's mixture-of-experts model",
      "context_window": 32768
    },
    {
      "id": "gemma2-9b-it",
      "name": "Gemma 2 9B",
      "description": "Google's efficient instruction-tuned model",
      "context_window": 8192
    }
  ],
  "default_model": "llama-3.3-70b-versatile",
  "current_model": null
}
```

**Use this endpoint to:**
- Populate model selection dropdown
- Show model capabilities to users

---

### POST `/api/chat/validate-model`

Validate if a model ID is available.

**Request Body:**
```json
{
  "model": "llama-3.3-70b-versatile"
}
```

**Response (valid):**
```json
{
  "model": "llama-3.3-70b-versatile",
  "valid": true,
  "available_models": null
}
```

**Response (invalid):**
```json
{
  "model": "invalid-model",
  "valid": false,
  "available_models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"]
}
```

---

## Data Types Reference

### Valid Symptoms

| Name | Display Name | Has Options |
|------|--------------|-------------|
| `fever` | Fever | pattern, severity |
| `chills` | Chills/Rigors | - |
| `sweating` | Profuse Sweating | - |
| `diarrhea` | Diarrhea | description, severity |
| `vomiting` | Vomiting | severity |
| `dehydration` | Dehydration | severity |
| `headache` | Headache | severity |
| `abdominal_pain` | Abdominal Pain | severity |
| `severe_abdominal_pain` | Severe Abdominal Pain | - |
| `constipation` | Constipation | - |
| `bitter_taste` | Bitter Taste | - |
| `rose_spots` | Rose Spots | - |
| `relative_bradycardia` | Relative Bradycardia | - |
| `altered_consciousness` | Altered Consciousness | - |
| `convulsions` | Convulsions/Seizures | - |
| `body_aches` | Body Aches | - |
| `dark_urine` | Dark/Bloody Urine | description |
| `anemia` | Anemia/Pallor | severity |
| `melena` | Melena | - |
| `bloody_stool` | Bloody Stool | - |

### Diarrhea Descriptions

| Value | Meaning | Associated Disease |
|-------|---------|-------------------|
| `rice_water` | Pale, milky with mucus flecks | Cholera (pathognomonic) |
| `watery` | Clear or yellow watery | Cholera, other |
| `bloody` | Visible blood | Various |
| `mucoid` | Containing mucus | Various |

### Fever Patterns

| Value | Description | Associated Disease |
|-------|-------------|-------------------|
| `cyclical` | Comes and goes (48-72hr cycles) | Malaria |
| `stepladder` | Gradually increasing daily | Typhoid |
| `continuous` | Persistent high fever | Various |
| `irregular` | No clear pattern | Various |

### Dehydration Findings

**mental_state:**
- `alert` - No dehydration
- `restless` / `irritable` - Some dehydration
- `lethargic` / `unconscious` - Severe dehydration

**eyes:**
- `normal` - No dehydration
- `sunken` - Some/Severe dehydration

**skin_pinch:**
- `normal` - No dehydration
- `slow` - Some dehydration  
- `very_slow` / `>2_seconds` - Severe dehydration

**thirst:**
- `drinks_normally` - No dehydration
- `drinks_eagerly` - Some dehydration
- `unable_to_drink` - Severe dehydration

### Lab Test Types

| Test | Disease | Positive Details |
|------|---------|------------------|
| `blood_smear` | Malaria | Species (e.g., "P. falciparum") |
| `rdt_malaria` | Malaria | - |
| `stool_culture` | Cholera | "vibrio cholerae" |
| `rdt_cholera` | Cholera | - |
| `blood_culture` | Typhoid | "salmonella typhi" |
| `widal` | Typhoid | Titer (e.g., "1:320") |
| `typhidot` | Typhoid | - |

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message here"
}
```

### Common HTTP Status Codes

| Code | Meaning | When |
|------|---------|------|
| `200` | Success | Request processed successfully |
| `400` | Bad Request | Invalid request body or parameters |
| `404` | Not Found | Resource doesn't exist |
| `422` | Validation Error | Pydantic validation failed |
| `500` | Server Error | Internal error (check logs) |

### Validation Error Response

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

## Integration Examples

### JavaScript/TypeScript (Fetch)

```typescript
// Expert System Diagnosis
async function diagnose(symptoms: Symptom[]) {
  const response = await fetch('http://localhost:8000/api/expert/diagnose', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ symptoms })
  });
  return response.json();
}

// AI Chat with conversation history
let conversationHistory: Message[] = [];

async function sendMessage(message: string) {
  const response = await fetch('http://localhost:8000/api/chat/message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      conversation_history: conversationHistory,
      include_expert_context: true
    })
  });
  
  const data = await response.json();
  conversationHistory = data.conversation_history;
  return data;
}
```

### React Hook Example

```typescript
import { useState } from 'react';

function useChat() {
  const [history, setHistory] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (message: string) => {
    setLoading(true);
    try {
      const res = await fetch('/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          conversation_history: history
        })
      });
      const data = await res.json();
      setHistory(data.conversation_history);
      return data;
    } finally {
      setLoading(false);
    }
  };

  const resetChat = () => setHistory([]);

  return { history, sendMessage, resetChat, loading };
}
```

### cURL Examples

```bash
# Health check
curl http://localhost:8000/api/ping

# Get symptoms list
curl http://localhost:8000/api/expert/symptoms

# Run diagnosis
curl -X POST http://localhost:8000/api/expert/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": [
      {"name": "fever", "present": true, "pattern": "cyclical"},
      {"name": "chills", "present": true}
    ],
    "patient": {"travel_endemic_area": true}
  }'

# Chat message
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have fever and chills for 3 days",
    "conversation_history": []
  }'
```

---

## CORS Configuration

The API has CORS enabled via `django-cors-headers`. For local development, all origins are typically allowed. In production, configure `CORS_ALLOWED_ORIGINS` in `settings.py`.

---

## Rate Limiting

Currently no rate limiting is implemented. For production:
- AI chat endpoints should be rate-limited (Groq has API limits)
- Consider implementing per-user/IP limits

---

## WebSocket Support (Future)

Streaming chat responses are planned for future versions. This will use:
- Endpoint: `ws://localhost:8000/api/chat/stream`
- Protocol: Server-Sent Events or WebSocket

---

## Questions?

- Check Swagger docs at `/api/docs` for interactive testing
- Review the [README.md](./README.md) for project overview
- Check source code in `src/api/routers/` for implementation details
