"""
Shared LLM configuration for all agents.
Handles switching between Vertex AI and Google AI Studio.
"""

from google.adk.models import Gemini
from config import settings

# Initialize the shared LLM instance
# If USE_VERTEXAI is True, it uses Vertex AI (requires ADC)
# If USE_VERTEXAI is False, it uses Google AI Studio (requires GOOGLE_API_KEY)
llm = Gemini(
    model=settings.MODEL_ID,
    api_key=settings.GOOGLE_API_KEY,
    vertexai=settings.USE_VERTEXAI,
    location=settings.LOCATION,
    project=settings.PROJECT_ID
)
