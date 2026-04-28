"""
Firestore service for persistent storage of sessions, user data, and election knowledge.
"""

import logging
from datetime import datetime, timezone
from typing import Any

from google.cloud import firestore

from config import settings

logger = logging.getLogger(__name__)


class FirestoreService:
    """Manages all Firestore operations for the election education platform."""

    def __init__(self):
        """Initialize Firestore client."""
        self._db = firestore.Client(
            project=settings.PROJECT_ID,
            database=settings.FIRESTORE_DATABASE,
        )
        logger.info("Firestore client initialized for project: %s", settings.PROJECT_ID)

    @property
    def db(self) -> firestore.Client:
        """Return the Firestore client instance."""
        return self._db

    # ── Session Management ──────────────────────────────────────────────

    async def create_session(self, user_id: str, session_id: str) -> dict:
        """Create a new chat session for a user."""
        session_data = {
            "user_id": user_id,
            "session_id": session_id,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "message_count": 0,
            "agents_used": [],
            "language": "en",
        }
        self._db.collection("sessions").document(session_id).set(session_data)
        logger.info("Created session %s for user %s", session_id, user_id)
        return session_data

    async def get_session(self, session_id: str) -> dict | None:
        """Retrieve a session by its ID."""
        doc = self._db.collection("sessions").document(session_id).get()
        return doc.to_dict() if doc.exists else None

    async def update_session(self, session_id: str, updates: dict) -> None:
        """Update session metadata."""
        updates["updated_at"] = datetime.now(timezone.utc)
        self._db.collection("sessions").document(session_id).update(updates)

    # ── Chat History ────────────────────────────────────────────────────

    async def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        agent_name: str | None = None,
    ) -> str:
        """Save a chat message to Firestore."""
        message_data = {
            "session_id": session_id,
            "role": role,
            "content": content,
            "agent_name": agent_name,
            "timestamp": datetime.now(timezone.utc),
        }
        doc_ref = (
            self._db.collection("sessions")
            .document(session_id)
            .collection("messages")
            .add(message_data)
        )
        message_id = doc_ref[1].id
        logger.debug("Saved message %s in session %s", message_id, session_id)
        return message_id

    async def get_chat_history(
        self, session_id: str, limit: int = 50
    ) -> list[dict]:
        """Retrieve chat history for a session."""
        messages = (
            self._db.collection("sessions")
            .document(session_id)
            .collection("messages")
            .order_by("timestamp")
            .limit(limit)
            .stream()
        )
        return [msg.to_dict() for msg in messages]

    # ── User Feedback ───────────────────────────────────────────────────

    async def save_feedback(
        self,
        session_id: str,
        message_id: str,
        rating: int,
        comment: str = "",
    ) -> None:
        """Save user feedback on a response."""
        feedback_data = {
            "session_id": session_id,
            "message_id": message_id,
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.now(timezone.utc),
        }
        self._db.collection("feedback").add(feedback_data)
        logger.info("Feedback saved for message %s", message_id)

    # ── Election Knowledge Base ─────────────────────────────────────────

    async def get_election_data(self, category: str) -> list[dict]:
        """Retrieve election knowledge base entries by category."""
        docs = (
            self._db.collection("election_knowledge")
            .where("category", "==", category)
            .stream()
        )
        return [doc.to_dict() for doc in docs]

    async def seed_election_data(self, data: list[dict]) -> int:
        """Seed the election knowledge base with initial data."""
        batch = self._db.batch()
        count = 0
        for item in data:
            ref = self._db.collection("election_knowledge").document()
            batch.set(ref, {**item, "created_at": datetime.now(timezone.utc)})
            count += 1
            if count % 400 == 0:  # Firestore batch limit is 500
                batch.commit()
                batch = self._db.batch()
        batch.commit()
        logger.info("Seeded %d election knowledge entries", count)
        return count


# Singleton instance
firestore_service = FirestoreService()
