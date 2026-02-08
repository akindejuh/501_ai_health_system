# Medical Expert System API

A Django-based medical diagnostic expert system with AI-powered conversational assistance for tropical diseases (Cholera, Malaria, Typhoid Fever).

## Project Overview

This project combines **rule-based expert system reasoning** with **LLM-powered conversational AI** to provide medical diagnostic guidance. It offers two interaction modes:

1. **Expert System (Structured)** - Direct, deterministic rule-based diagnosis via structured API endpoints
2. **AI Chat (Conversational)** - Natural language interaction with an AI assistant that references expert system knowledge

### Supported Diseases

| Disease | Causative Agent | Transmission |
|---------|-----------------|--------------|
| **Cholera** | *Vibrio cholerae* | Contaminated water/food |
| **Malaria** | *Plasmodium* species | Infected mosquitoes |
| **Typhoid Fever** | *Salmonella typhi* | Contaminated water/food |

### Key Features

- ✅ Rule-based expert system using [Experta](https://github.com/nilp0inter/experta) knowledge engine
- ✅ WHO dehydration classification protocol (Plans A/B/C)
- ✅ AI chat powered by Groq API (Llama 3.3, Mixtral, Gemma models)
- ✅ Knowledge base RAG from curated medical markdown files
- ✅ Confidence-level diagnosis (confirmed → confident → suspect → uncertain)
- ✅ Swagger/OpenAPI documentation at `/api/docs`

---

## Project Structure

```
use_experta/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API keys)
├── Makefile                  # Common commands
│
├── src/
│   ├── config/               # Django configuration
│   │   ├── settings.py       # Django settings (loads .env)
│   │   ├── urls.py           # URL routing
│   │   ├── wsgi.py           # WSGI application
│   │   └── asgi.py           # ASGI application
│   │
│   ├── api/                  # API layer (Django Ninja)
│   │   ├── api.py            # Main API configuration
│   │   ├── routers/
│   │   │   ├── expert.py     # Expert system endpoints
│   │   │   └── chat.py       # AI chat endpoints
│   │   └── schemas/
│   │       ├── expert.py     # Pydantic models for expert API
│   │       └── chat.py       # Pydantic models for chat API
│   │
│   └── lib/
│       ├── expert_system/    # Core expert system
│       │   ├── diagnosis_engine.py  # Experta KnowledgeEngine with rules
│       │   ├── facts.py             # Fact definitions (Symptom, Patient, etc.)
│       │   ├── main.py              # Interactive console interface
│       │   ├── visualize_knowledge.py
│       │   └── raw_knowledge/       # Medical knowledge markdown files
│       │       ├── cholera/
│       │       ├── malaria/
│       │       └── typhoid_fever/
│       │
│       └── ai/               # AI/LLM layer
│           ├── llm_client.py      # Groq API client
│           ├── knowledge_base.py  # RAG knowledge retrieval
│           └── prompts.py         # System prompts with expert rules
│
└── env/                      # Python virtual environment
```

---

## Installation & Setup

### Prerequisites

- **Python 3.8.x** (specifically 3.8, NOT 3.9+)
  - ⚠️ The `experta` library uses `collections.Mapping` which was removed in Python 3.10
  - Python 3.9 deprecated it, Python 3.10+ will throw `AttributeError: module 'collections' has no attribute 'Mapping'`
- pip

### 1. Clone and Setup Virtual Environment

```bash
cd use_experta

# Create virtual environment (if not exists)
python -m venv env

# Activate virtual environment
# Windows (Git Bash/MINGW):
source env/Scripts/activate
# Windows (CMD):
env\Scripts\activate.bat
# Linux/Mac:
source env/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

# Additional dependencies (if not in requirements.txt):
pip install httpx python-dotenv
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
OPEN_API_BASE_URL=https://api.groq.com/openai/v1
```

Get a free Groq API key at: https://console.groq.com/

### 4. Run the Server

```bash
python manage.py runserver
```

The API will be available at: http://127.0.0.1:8000/api/

---

## API Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API info and status |
| `/api/ping` | GET | Health check |
| `/api/docs` | GET | Swagger documentation |
| `/api/expert/diagnose` | POST | Run expert system diagnosis |
| `/api/expert/symptoms` | GET | List valid symptoms |
| `/api/expert/diseases` | GET | List supported diseases |
| `/api/expert/diseases/{name}` | GET | Get disease details |
| `/api/chat/message` | POST | Send chat message to AI |
| `/api/chat/models` | GET | List available LLM models |
| `/api/chat/validate-model` | POST | Validate model selection |

See [endpoints_doc.md](./endpoints_doc.md) for detailed API documentation.

---

## Architecture

### Expert System Layer

The expert system uses **Experta** (a Python port of CLIPS) with production rules:

```
IF (rice-water stool) AND (severe dehydration)
THEN diagnosis = cholera (confident)
```

**Confidence Levels:**
- `confirmed` - Lab-verified diagnosis
- `confident` - Pathognomonic clinical signs present
- `suspect` - Clinical suspicion based on symptoms + exposure
- `uncertain` - Insufficient findings

### AI Layer

The AI chat uses **Groq API** with:
- System prompt embedding expert system rules
- RAG retrieval from medical knowledge markdown files
- Symptom extraction from conversation
- Model switching (Llama 3.3 70B default)

```
User Message → Extract Symptoms → Retrieve Knowledge → LLM + Expert Context → Response
```

---

## Development

### Running Tests

```bash
python manage.py test
```

### Interactive Expert System (CLI)

```bash
cd src/lib/expert_system
python -m main
```

### Adding New Diseases

1. Add knowledge files in `src/lib/expert_system/raw_knowledge/{disease_name}/`
2. Add Experta rules in `diagnosis_engine.py`
3. Update `DISEASES` dict in `src/api/routers/expert.py`
4. Update prompts in `src/lib/ai/prompts.py`

---

## TODO / Roadmap

### Phase 1 - Core (✅ Complete)
- [x] Expert system with Experta rules
- [x] Django Ninja API setup
- [x] Expert system API endpoints
- [x] AI chat integration with Groq
- [x] Knowledge base RAG
- [x] Swagger documentation

### Phase 2 - Enhancements
- [ ] Add more diseases (Dengue, Typhus, etc.)
- [ ] Implement conversation persistence (database)
- [ ] Add user authentication
- [ ] Rate limiting for AI endpoints
- [ ] Streaming responses for chat
- [ ] Vector embeddings for better RAG (using sentence-transformers)

### Phase 3 - Production
- [ ] Docker containerization
- [ ] Production deployment guide (Vercel/Railway)
- [ ] Monitoring and logging
- [ ] Admin dashboard
- [ ] Multi-language support

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Python | 3.8.x (required for experta) |
| Backend Framework | Django 4.2 |
| API Layer | Django Ninja |
| Expert System | Experta 1.9.4 |
| LLM Provider | Groq (Llama 3.3, Mixtral, Gemma) |
| HTTP Client | httpx (async) |
| Validation | Pydantic |
| Database | SQLite (development) |
| Container | Docker (python:3.8-slim) |

---

## License

This project is for educational purposes. Medical information provided is not a substitute for professional medical advice.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test
4. Submit a pull request

---

## Disclaimer

⚠️ **This is an educational expert system, not a medical device.**

The diagnostic suggestions provided by this system are for informational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition.
