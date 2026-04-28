# Architecture Documentation

## System Architecture

### Overview

Chunav Mitra uses a **multi-agent architecture** built on Google's Agent Development Kit (ADK). The system consists of:

1. **Root Orchestrator Agent** — Routes queries to specialist agents
2. **6 Specialist Agents** — Each handling a specific election education domain
3. **Tool Functions** — Provide structured, factual data to agents
4. **FastAPI Backend** — Exposes REST/SSE APIs for the frontend
5. **React Frontend** — Premium glassmorphic chat interface
6. **Cloud Firestore** — Persistent storage for sessions and chat history

### Agent Communication Flow

```
User Query → FastAPI → ADK Runner → Root Agent (Chunav Mitra)
                                         │
                                         ├─→ election_system_agent
                                         ├─→ parliament_guide_agent
                                         ├─→ voter_registration_agent
                                         ├─→ candidate_info_agent
                                         ├─→ language_assist_agent
                                         └─→ voting_day_agent
                                              │
                                              ├─→ Tool Functions (structured data)
                                              └─→ Gemini 2.0 Flash (reasoning)
                                                   │
                                                   └─→ Response → User
```

### Data Flow

1. User sends message via React frontend
2. FastAPI receives request and creates ADK Content object
3. ADK Runner passes message to root agent
4. Root agent analyzes intent and delegates to specialist
5. Specialist agent calls relevant tool functions for data
6. Gemini model synthesizes tool data into natural language
7. Response streamed back via SSE or returned as JSON
8. Message pair saved to Firestore for history

### Security Model

- Authentication: GCP IAM (service account for Cloud Run)
- CORS: Whitelist-based origin filtering
- Input: Pydantic validation with length limits
- Output: Agents instructed to be non-partisan and factual
- Storage: No PII beyond session identifiers

### Scaling

- Cloud Run auto-scales 0-5 instances
- Firestore handles concurrent sessions natively
- Gemini API rate limits managed by ADK
- Frontend served as static assets (can use Cloud CDN)
