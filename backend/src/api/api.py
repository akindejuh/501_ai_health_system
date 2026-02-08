"""
Medical Expert API.

Production-grade API for medical diagnostics with AI-powered chat assistance.
"""
from ninja import NinjaAPI

from .routers import expert_router, chat_router

# Initialize API with metadata
api = NinjaAPI(
    title="Medical Expert API",
    version="1.0.0",
    description="""
## Medical Diagnostic Expert System API

This API provides two modes of interaction:

### 1. Expert System (Structured)
Use `/expert/*` endpoints for direct, structured interaction with the rule-based 
expert system. Best for:
- Programmatic integration
- Structured symptom input
- Deterministic rule-based reasoning

### 2. AI Chat (Conversational)  
Use `/chat/*` endpoints for natural language interaction with an AI assistant
that references the expert system knowledge. Best for:
- End-user facing applications
- Exploratory symptom discussion
- Natural language queries

### Supported Diseases
- **Cholera** - Acute watery diarrhea caused by *Vibrio cholerae*
- **Malaria** - Parasitic disease caused by *Plasmodium* species
- **Typhoid Fever** - Enteric fever caused by *Salmonella typhi*

### Disclaimer
This system is for educational and informational purposes only. 
Always consult a healthcare professional for medical advice.
    """,
    docs_url="/docs",
)

# Register routers
api.add_router("/expert", expert_router)
api.add_router("/chat", chat_router)


@api.get("/ping", tags=["Health & Info"], summary="Simple ping check")
def ping(request):
    """Simple endpoint to check if the API is responding."""
    return {"message": "pong"}


@api.get("/", tags=["Health & Info"], summary="API info")
def root(request):
    """Return basic API information."""
    return {
        "name": "Medical Expert API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs",
        "endpoints": {
            "expert": "/api/expert - Structured expert system access",
            "chat": "/api/chat - AI-powered conversational assistant",
        }
    }
