# 🗳️ Election Buddy — India Election Process Education Assistant

> **PromptWars 2 | Problem Statement: Election Process Education**
>
> An AI-powered assistant that helps users understand India's election process, timelines, and steps in an interactive and easy-to-follow way.

---

## 🌐 Live Production Links

*   **Main Application**: [https://election-buddy-ui-d3kidpb2jq-uc.a.run.app](https://election-buddy-ui-d3kidpb2jq-uc.a.run.app)

---

## 📋 Chosen Vertical

**Election Process Education** — Create an assistant that helps users understand the election process, timelines, and steps in an interactive and easy-to-follow way.

**Election Buddy** 🇮🇳 is a production-ready, AI-powered platform designed to educate Indian citizens about the election process. Built using the **Google Agent Development Kit (ADK)** and **Gemini 3 Flash**, it provides a hierarchical multi-agent assistant that can answer complex questions about voter registration, candidate research, parliament procedures, and voting day logistics.

## 🌟 Key Features

*   **Hierarchical Multi-Agent Architecture**: 6 specialist agents orchestrated by a root agent 🇮🇳.
*   **Dual-Backend Flexibility**: Supports both **Vertex AI** and **Google AI Studio** (via API Key).
*   **Premium Glassmorphic UI**: High-performance React frontend with an Indian tricolor design system.
*   **Real-time Interaction**: Streaming responses (SSE) for a seamless educational experience.

---

## 🎯 Approach and Logic

### Problem Analysis

India's election process presents several challenges for citizens:

| # | Challenge | Our Solution |
|---|-----------|-------------|
| 1 | Complexity of multi-level elections (national, state, local) | **Election System Agent** — Explains the 3-tier structure with ECI framework |
| 2 | Confusion between Lok Sabha and Rajya Sabha | **Parliament Guide Agent** — Side-by-side comparisons and role clarity |
| 3 | Voter registration difficulties on NVSP | **Voter Registration Agent** — Step-by-step NVSP portal guidance |
| 4 | Limited candidate awareness | **Candidate Info Agent** — Disclosure lookup via MyNeta.info, PRS India |
| 5 | Language and literacy barriers | **Language Assist Agent** — Simplified explanations, symbol-based guidance |
| 6 | Voting day logistics confusion | **Voting Day Agent** — Checklist, EVM guide, document requirements |

### Architecture Design

```
┌─────────────────────────────────────────────────┐
│                  React Frontend                  │
│         (Vite + Glassmorphic UI)                │
└──────────────────────┬──────────────────────────┘
                       │ REST API / SSE
┌──────────────────────▼──────────────────────────┐
│              FastAPI Backend (Cloud Run)          │
│  ┌─────────────────────────────────────────┐    │
│  │       Root Orchestrator Agent            │    │
│  │              Google ADK                  │    │
│  └──┬───┬───┬───┬───┬───┬──────────────────┘    │
│     │   │   │   │   │   │                        │
│  ┌──▼┐┌─▼┐┌─▼┐┌─▼┐┌─▼┐┌─▼┐                    │
│  │ES ││PG││VR││CI││LA││VD│  ← 6 Specialist     │
│  │   ││  ││  ││  ││  ││  │    ADK Agents       │
│  └───┘└──┘└──┘└──┘└──┘└──┘                     │
│     │   │   │   │   │   │                        │
│  ┌──▼───▼───▼───▼───▼───▼──┐                    │
│  │    Tool Functions         │                    │
│  │  (Election Data, Voter,   │                    │
│  │   Candidate Tools)        │                    │
│  └──────────┬────────────────┘                    │
└─────────────┼────────────────────────────────────┘
              │
    ┌─────────▼─────────┐    ┌──────────────────┐
    │  Cloud Firestore   │    │  Google AI SDK   │
    │  (Sessions, Chat   │    │  Gemini 3 Flash  │
    │   History, KB)     │    │ (API Key/Vertex) │
    └────────────────────┘    └──────────────────┘
```

**Agent Key:** ES=Election System, PG=Parliament Guide, VR=Voter Registration, CI=Candidate Info, LA=Language Assist, VD=Voting Day

### Multi-Agent Strategy

The system uses **ADK's `sub_agents` architecture** where a root orchestrator agent (`Election Buddy`) automatically routes user queries to the most appropriate specialist agent based on the query context. Each agent has:

- **Domain-specific instructions** — Expert system prompts tailored to their specialty
- **Dedicated tools** — Python functions providing structured, factual election data
- **Focused scope** — Clear boundaries preventing hallucination

---

## 🔧 How the Solution Works

### 1. User Interaction Flow

```
User asks question → React Frontend → FastAPI Backend
                                          │
                              ADK Runner processes query
                                          │
                              Root Agent routes to specialist
                                          │
                              Specialist Agent + Tools generate response
                                          │
                              Response saved to Firestore
                                          │
                              Streamed back to React Frontend
```

### 2. Backend (FastAPI + ADK)

- **`main.py`** — FastAPI application with REST and SSE streaming endpoints
- **`agents/orchestrator.py`** — Root agent with 6 sub-agents using `google.adk.agents.Agent`
- **`agents/llm_config.py`** — Centralized AI configuration for Vertex AI / AI Studio
- **`agents/*.py`** — 6 specialist agents, each with domain-specific instructions
- **`tools/*.py`** — Pure Python functions returning structured election data
- **`services/firestore_service.py`** — Firestore integration for sessions and chat history

### 3. Frontend (React + Vite)

- **Welcome Screen** — Agent cards and quick action buttons for discovery
- **Chat Interface** — Real-time messaging with markdown rendering
- **Sidebar** — Agent navigation and session management
- **Responsive Design** — Mobile-first glassmorphic UI with Indian tricolor theme

### 4. Google Cloud Integration

| Service | Usage |
|---------|-------|
| **Vertex AI / Gemini 3 Flash** | LLM backbone for all 6 agents |
| **Google ADK** | Agent framework with multi-agent orchestration |
| **Cloud Firestore** | Session storage, chat history, user feedback |
| **Cloud Run** | Containerized backend and frontend deployment |
| **Cloud Build** | CI/CD pipeline for Docker image builds |
| **Artifact Registry** | Docker image storage |

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, Vite 8, Vanilla CSS |
| **Backend** | Python 3.12, FastAPI, Uvicorn |
| **AI/ML** | Google ADK, Gemini 3 Flash, Vertex AI / AI Studio |
| **Database** | Cloud Firestore (Native mode) |
| **Infrastructure** | Docker, Cloud Run, Cloud Build |
| **Testing** | Pytest, FastAPI TestClient |

---

## 📁 Project Structure

```
P2-India-Election/
├── README.md
├── .gitignore
├── backend/
│   ├── Dockerfile              # Production container
│   ├── requirements.txt        # Python dependencies
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Environment configuration
│   ├── agents/
│   │   ├── orchestrator.py     # Root agent (Election Buddy)
│   │   ├── llm_config.py       # Centralized AI config
│   │   ├── election_system_agent.py
│   │   ├── parliament_guide_agent.py
│   │   ├── voter_registration_agent.py
│   │   ├── candidate_info_agent.py
│   │   ├── language_assist_agent.py
│   │   └── voting_day_agent.py
│   ├── tools/
│   │   ├── election_data.py    # Election structure & timeline data
│   │   ├── voter_tools.py      # NVSP & registration guides
│   │   └── candidate_tools.py  # Candidate disclosure & voting day
│   ├── services/
│   │   └── firestore_service.py
│   └── tests/
│       ├── test_tools.py       # Tool function tests
│       └── test_api.py         # API endpoint tests
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── App.css
│       ├── index.css           # Design system
│       ├── components/
│       │   ├── Header.jsx
│       │   ├── Sidebar.jsx
│       │   ├── ChatInterface.jsx
│       │   └── WelcomeScreen.jsx
│       └── services/
│           └── api.js
├── scripts/
│   ├── setup_gcp.sh           # GCP resource provisioning
│   └── deploy.sh              # Cloud Run deployment
└── docs/
    └── architecture.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- Google Cloud SDK (`gcloud`)
- GCP Project with billing enabled
- **Google AI Studio API Key** (optional, for non-Vertex deployments)

### 1. Setup GCP Resources

```bash
chmod +x scripts/setup_gcp.sh
./scripts/setup_gcp.sh
```

### 2. Run Backend Locally

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Update .env with GOOGLE_API_KEY
python main.py
```

### 3. Run Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

### 4. Deploy to Cloud Run

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

---

## 🧪 Testing

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v --cov=tools --cov=services
```

### Test Coverage

- **30+ unit tests** covering all tool functions
- **API endpoint tests** with mocked Firestore
- **Eligibility validation tests** for edge cases
- **Data structure tests** ensuring correct schemas

---

## 🔒 Security

- **No hardcoded credentials** — All secrets via environment variables
- **CORS configured** — Only allowed origins can access the API
- **Input validation** — Pydantic models enforce request schemas
- **Rate limiting ready** — Cloud Run handles scaling
- **Non-partisan** — Agents are instructed to remain strictly factual and unbiased
- **No PII storage** — Only session IDs and chat content stored

---

## ♿ Accessibility

- **ARIA labels** on all interactive elements
- **Keyboard navigation** — Full tab support and Enter key actions
- **Screen reader support** — Role attributes and live regions
- **Reduced motion** — Respects `prefers-reduced-motion`
- **Color contrast** — WCAG AA compliant color scheme
- **Semantic HTML** — Proper heading hierarchy and landmark regions
- **Responsive design** — Mobile-first approach (320px to 4K)

---

## 📐 Assumptions

1. **Educational Purpose Only** — This tool provides election education, not official election services. Users should verify information with official ECI sources.
2. **English Primary** — The primary interface is in English with Hindi labels. The Language Assist Agent can explain concepts in simpler terms.
3. **Data Currency** — Election data reflects the latest available information as of the 2024 General Elections. Data tools contain structured, factual information that doesn't require real-time API calls.
4. **GCP Project** — A GCP project (`p2-india-election`) with billing enabled is assumed for deployment.
5. **Gemini Model** — The system uses `gemini-2.0-flash` for optimal speed and cost. Can be changed via environment variable.
6. **No Real-Time Data** — Candidate information tools guide users to official sources (MyNeta.info, ECI) rather than scraping live data.

---

## 📊 Evaluation Alignment

| Criteria | Implementation |
|----------|---------------|
| **Code Quality** | Modular architecture, type hints, docstrings, clean separation of concerns |
| **Security** | Env-based config, CORS, input validation, no PII, non-partisan design |
| **Efficiency** | Lightweight agents, structured tool data (no redundant API calls), SSE streaming |
| **Testing** | 30+ pytest tests, API tests with mocks, comprehensive tool validation |
| **Accessibility** | ARIA labels, keyboard nav, screen readers, reduced motion, responsive |
| **Google Services** | ADK, Gemini, Firestore, Cloud Run, Vertex AI, Cloud Build, Artifact Registry |
| **Problem Alignment** | 6 agents addressing all 6 identified challenges in election education |

---

## 📜 License

MIT License — Built for PromptWars 2

---

<p align="center">
  <strong>🇮🇳 Every vote counts. Every voter matters. 🇮🇳</strong><br>
  <em>Built with ❤️ using Google ADK & Gemini</em>
</p>
