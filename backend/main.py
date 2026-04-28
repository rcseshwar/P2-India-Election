"""
India Election Process Education - FastAPI Backend
Main application entry point with ADK agent integration.
"""

import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.orchestrator import root_agent
from config import settings
from services.firestore_service import firestore_service

# ── Logging ─────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ── ADK Session & Runner ────────────────────────────────────────────────

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=settings.APP_NAME,
    session_service=session_service,
)


# ── Lifespan ────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info("🗳️  Chunav Mitra backend starting...")
    logger.info("Project: %s | Model: %s", settings.PROJECT_ID, settings.MODEL_ID)
    yield
    logger.info("Chunav Mitra backend shutting down.")


# ── FastAPI App ─────────────────────────────────────────────────────────

app = FastAPI(
    title="Election Buddy 🇮🇳 - India Election Education API",
    description="AI-powered assistant for Indian election process education using Google ADK 🇮🇳",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response Models ───────────────────────────────────────────

class ChatRequest(BaseModel):
    """Chat message request from the frontend."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    session_id: str | None = Field(None, description="Existing session ID to continue conversation")
    user_id: str = Field(default="anonymous", description="User identifier")
    language: str = Field(default="en", description="Preferred language code")


class ChatResponse(BaseModel):
    """Chat response returned to the frontend."""
    response: str
    session_id: str
    agent_name: str | None = None
    sources: list[str] = []


class SessionResponse(BaseModel):
    """Session information response."""
    session_id: str
    created: bool
    message_count: int = 0


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    project_id: str
    model: str


class FeedbackRequest(BaseModel):
    """User feedback on a response."""
    session_id: str
    message_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: str = ""


# ── API Routes ──────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint for Cloud Run."""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        project_id=settings.PROJECT_ID,
        model=settings.MODEL_ID,
    )


@app.post("/api/session", response_model=SessionResponse, tags=["Session"])
async def create_session(user_id: str = "anonymous"):
    """Create a new chat session."""
    session_id = str(uuid.uuid4())
    try:
        # Create ADK session
        await session_service.create_session(
            app_name=settings.APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )
        # Persist to Firestore
        await firestore_service.create_session(user_id, session_id)
        logger.info("Created session: %s", session_id)
        return SessionResponse(session_id=session_id, created=True)
    except Exception as e:
        logger.error("Failed to create session: %s", e)
        raise HTTPException(status_code=500, detail="Failed to create session") from e


@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """Send a message and get a response from Chunav Mitra."""
    try:
        # Create session if not provided
        session_id = request.session_id
        if not session_id:
            session_id = str(uuid.uuid4())
            await session_service.create_session(
                app_name=settings.APP_NAME,
                user_id=request.user_id,
                session_id=session_id,
            )
            await firestore_service.create_session(request.user_id, session_id)

        # Save user message to Firestore
        await firestore_service.save_message(
            session_id=session_id,
            role="user",
            content=request.message,
        )

        # Create content for the agent
        user_content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=request.message)],
        )

        # Run the agent
        final_response = ""
        agent_name = None

        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session_id,
            new_message=user_content,
        ):
            if event.is_final_response():
                for part in event.content.parts:
                    if part.text:
                        final_response += part.text
                agent_name = event.author

        if not final_response:
            final_response = "I'm sorry, I couldn't process your question. Please try rephrasing it."

        # Save agent response to Firestore
        await firestore_service.save_message(
            session_id=session_id,
            role="assistant",
            content=final_response,
            agent_name=agent_name,
        )

        logger.info("Chat response from agent '%s' for session %s", agent_name, session_id)

        return ChatResponse(
            response=final_response,
            session_id=session_id,
            agent_name=agent_name,
        )

    except Exception as e:
        logger.error("Chat error: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process message: {str(e)}",
        ) from e


@app.post("/api/chat/stream", tags=["Chat"])
async def chat_stream(request: ChatRequest):
    """Stream a response from Chunav Mitra (Server-Sent Events)."""

    async def event_generator():
        try:
            session_id = request.session_id
            if not session_id:
                session_id = str(uuid.uuid4())
                await session_service.create_session(
                    app_name=settings.APP_NAME,
                    user_id=request.user_id,
                    session_id=session_id,
                )

            user_content = types.Content(
                role="user",
                parts=[types.Part.from_text(text=request.message)],
            )

            yield f"data: {{\"type\":\"session\",\"session_id\":\"{session_id}\"}}\n\n"

            full_response = ""
            agent_name = None

            async for event in runner.run_async(
                user_id=request.user_id,
                session_id=session_id,
                new_message=user_content,
            ):
                if event.is_final_response():
                    for part in event.content.parts:
                        if part.text:
                            full_response += part.text
                            import json
                            chunk_data = json.dumps({
                                "type": "chunk",
                                "content": part.text,
                                "agent": event.author,
                            })
                            yield f"data: {chunk_data}\n\n"
                    agent_name = event.author

            # Save to Firestore
            await firestore_service.save_message(
                session_id=session_id, role="user", content=request.message
            )
            await firestore_service.save_message(
                session_id=session_id,
                role="assistant",
                content=full_response,
                agent_name=agent_name,
            )

            yield f"data: {{\"type\":\"done\"}}\n\n"

        except Exception as e:
            logger.error("Stream error: %s", e, exc_info=True)
            import json
            error_data = json.dumps({"type": "error", "message": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/history/{session_id}", tags=["Chat"])
async def get_history(session_id: str, limit: int = 50):
    """Retrieve chat history for a session."""
    try:
        messages = await firestore_service.get_chat_history(session_id, limit)
        return {"session_id": session_id, "messages": messages}
    except Exception as e:
        logger.error("History retrieval error: %s", e)
        raise HTTPException(status_code=500, detail="Failed to retrieve history") from e


@app.post("/api/feedback", tags=["Feedback"])
async def submit_feedback(request: FeedbackRequest):
    """Submit user feedback on a response."""
    try:
        await firestore_service.save_feedback(
            session_id=request.session_id,
            message_id=request.message_id,
            rating=request.rating,
            comment=request.comment,
        )
        return {"status": "ok", "message": "Feedback saved successfully"}
    except Exception as e:
        logger.error("Feedback error: %s", e)
        raise HTTPException(status_code=500, detail="Failed to save feedback") from e


@app.get("/api/agents", tags=["System"])
async def list_agents():
    """List all available specialist agents."""
    agents = [
        {
            "name": "election_system_agent",
            "title": "Election System Expert 🇮🇳",
            "icon": "📊",
            "description": "India's multi-level election system (national, state, local)",
            "topics": ["ECI", "Election phases", "Constitutional framework", "Delimitation"],
        },
        {
            "name": "parliament_guide_agent",
            "title": "Parliament Guide 🇮🇳",
            "icon": "🏛️",
            "description": "Lok Sabha vs Rajya Sabha, law-making process",
            "topics": ["Lok Sabha", "Rajya Sabha", "Bills", "Joint Sessions", "Government formation"],
        },
        {
            "name": "voter_registration_agent",
            "title": "Voter Registration Helper 🇮🇳",
            "icon": "📝",
            "description": "Register to vote, check status, get e-EPIC",
            "topics": ["NVSP", "Form 6", "e-EPIC", "Eligibility", "BLO verification"],
        },
        {
            "name": "candidate_info_agent",
            "title": "Candidate Research Advisor 🇮🇳",
            "icon": "🔍",
            "description": "Research candidate backgrounds and disclosures",
            "topics": ["Criminal records", "Asset declarations", "Performance", "MyNeta.info"],
        },
        {
            "name": "language_assist_agent",
            "title": "Language & Accessibility Guide 🇮🇳",
            "icon": "🗣️",
            "description": "Simple explanations and expert support",
            "topics": ["EVM guide", "Party symbols", "NOTA", "Braille EVMs"],
        },
        {
            "name": "voting_day_agent",
            "title": "Voting Day Companion 🇮🇳",
            "icon": "📅",
            "description": "Polling day preparation and booth procedures",
            "topics": ["Checklist", "Documents", "EVM usage", "VVPAT", "cVIGIL"],
        },
    ]
    return {"agents": agents}


# ── Main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
