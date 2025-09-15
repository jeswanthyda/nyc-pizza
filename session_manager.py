from typing import Optional

from backend.client import FastAPIClient
from logging_utils import get_logger

logger = get_logger(__name__)


class SessionManager:
    """Manages game session lifecycle and API communication."""

    def __init__(self):
        """Initialize the session manager."""
        self.session_id: Optional[str] = None
        self.api_client: Optional[FastAPIClient] = None
        self._initialize_api_client()

    def _initialize_api_client(self):
        """Initialize the FastAPI client for session logging."""
        try:
            self.api_client = FastAPIClient()
            # Test connection
            if self.api_client.health_check():
                logger.info("Connected to FastAPI server for session logging")
            else:
                logger.warning(
                    "FastAPI server not available - sessions will not be logged"
                )
                self.api_client = None
        except Exception as e:
            logger.warning(f"Failed to initialize API client: {e}")
            self.api_client = None

    def create_session(
        self, player_name: str, earned: float = 0.0, spent: float = 0.0
    ) -> bool:
        """Create a new session in the database."""
        if not self.api_client:
            return False

        try:
            session_response = self.api_client.create_session(
                player_name=player_name, earned=earned, spent=spent
            )
            if session_response:
                self.session_id = session_response.session_id
                logger.info(f"Session created with ID: {self.session_id}")
                return True
            else:
                logger.error("Failed to create session")
                return False
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return False

    def update_session(self, earned: float, spent: float) -> bool:
        """Update the current session with final scores."""
        if not self.api_client or not self.session_id:
            return False

        try:
            session_response = self.api_client.update_session(
                session_id=self.session_id, earned=earned, spent=spent
            )
            if session_response:
                logger.info(
                    f"Session updated: Net Income ${session_response.net_income}"
                )
                return True
            else:
                logger.error("Failed to update session")
                return False
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            return False

    def cleanup(self):
        """Clean up the API client resources."""
        if self.api_client:
            try:
                self.api_client.client.close()
                self.api_client = None
            except Exception as e:
                logger.error(f"Error cleaning up API client: {e}")

    def reset_session(self):
        """Reset the session ID for a new game."""
        self.session_id = None
