# Medical Expert System

A hybrid diagnostic assistance platform that combines **rule-based expert system reasoning** with **LLM-powered conversational AI** for tropical disease diagnosis (Cholera, Malaria, Typhoid Fever).

Built for healthcare workers in endemic regions who face limited specialist access and high patient volumes.

## How It Works

The system offers two interaction modes:

- **Expert System (Structured)** — Deterministic, rule-based diagnosis using WHO clinical guidelines via the [Experta](https://github.com/nilp0inter/experta) engine. Works offline, returns results in milliseconds.
- **AI Chat (Conversational)** — Natural language interface powered by Groq LLMs (Llama 3.3, Mixtral, Gemma) with RAG retrieval from curated medical knowledge files.

## Project Structure

```
.
├── backend/          # Python/Django API (expert system + AI chat)
│   ├── src/
│   │   ├── config/   # Django settings, ASGI
│   │   ├── api/      # Django Ninja routes & schemas
│   │   └── lib/      # Expert system engine, AI/LLM client, knowledge base
│   ├── Dockerfile
│   └── Makefile
│
├── frontend/         # Next.js web client
│   ├── app/
│   ├── components/
│   ├── Dockerfile
│   └── Makefile
│
├── docker-compose.yml
└── Makefile          # Root commands for the full stack
```

## Prerequisites

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.8.x | Required — `experta` uses `collections.Mapping` removed in 3.10+ |
| Node.js | 20+ | For the frontend |
| pnpm | 10+ | Frontend package manager |
| Docker | 20+ | Optional, for containerized setup |

## Getting Started

### 1. Clone the repo

```bash
git clone <repo-url>
cd 501_ai_health_system
```

### 2. Set up environment variables

Copy the example files and fill in your keys:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

**Backend** (`backend/.env`):
```
GROQ_API_KEY=your_groq_api_key_here
OPEN_API_BASE_URL=https://api.groq.com/openai/v1
```

Get a free Groq API key at https://console.groq.com/

**Frontend** (`frontend/.env`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 3. Run the services

#### Option A: Docker (recommended)

```bash
make up
```

This starts both services:
- Backend at http://localhost:8000
- Frontend at http://localhost:3000

To stop:

```bash
make down
```

#### Option B: Run locally

**Backend:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
make dev
```

**Frontend** (in a separate terminal):

```bash
cd frontend
pnpm install
pnpm dev
```

### 4. Verify

- API docs (Swagger): http://localhost:8000/api/docs
- Frontend: http://localhost:3000
- Health check: http://localhost:8000/api/ping

## Available Commands

From the project root:

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies for both services |
| `make dev-backend` | Start backend dev server |
| `make dev-frontend` | Start frontend dev server |
| `make build` | Build both services |
| `make up` | Start all services with Docker |
| `make up-d` | Start all services in background |
| `make down` | Stop Docker services |

## API Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/docs` | GET | Swagger documentation |
| `/api/expert/diagnose` | POST | Run expert system diagnosis |
| `/api/expert/symptoms` | GET | List valid symptoms |
| `/api/expert/diseases` | GET | List supported diseases |
| `/api/chat/message` | POST | Send message to AI assistant |
| `/api/chat/models` | GET | List available LLM models |

See [backend/endpoints_doc.md](backend/endpoints_doc.md) for the full API reference.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.8, Django 4.2, Django Ninja |
| Expert System | Experta 1.9.4 (CLIPS-based rule engine) |
| AI/LLM | Groq API (Llama 3.3 70B default) |
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS 4 |
| Package Manager | pnpm (frontend), pip (backend) |
| Containerization | Docker, Docker Compose |

## Disclaimer

This is an educational expert system, **not a certified medical device**. Diagnostic suggestions are for informational purposes only and should not replace professional medical advice. Always consult a qualified healthcare provider.

## License

See [LICENSE](LICENSE).
