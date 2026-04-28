"""
Application configuration module.
Centralizes all environment variables and settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # GCP Configuration
    PROJECT_ID: str = os.getenv("GOOGLE_CLOUD_PROJECT", "p2-india-election")
    LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    # Gemini Model
    MODEL_ID: str = os.getenv("MODEL_ID", "gemini-1.5-flash")

    # Firestore
    FIRESTORE_DATABASE: str = os.getenv("FIRESTORE_DATABASE", "(default)")

    # Application
    APP_NAME: str = "india-election-educator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # CORS
    ALLOWED_ORIGINS: list[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:5173"
    ).split(",")

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8080"))


settings = Settings()
