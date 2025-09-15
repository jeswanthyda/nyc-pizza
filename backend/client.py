"""FastAPI client for logging game sessions to the database."""

import sys
import uuid
from pathlib import Path
from typing import Optional

import httpx

# Add parent directory to path to import logging_utils
sys.path.append(str(Path(__file__).parent.parent))
from logging_utils import get_logger

from .db.models import Session
from .server.schemas import SessionCreate, SessionUpdate


class FastAPIClient:
    """Client for communicating with the FastAPI server."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the client with the server base URL."""
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=10.0)
        self.logger = get_logger(__name__)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close the HTTP client."""
        self.client.close()

    def health_check(self) -> bool:
        """Check if the server is healthy."""
        try:
            response = self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except httpx.RequestError:
            return False

    def _make_request(
        self,
        method: str,
        endpoint: str,
        operation_name: str,
        json_data: Optional[dict] = None,
    ) -> Optional[dict]:
        """Make an HTTP request with common error handling."""
        try:
            response = self.client.request(
                method, f"{self.base_url}{endpoint}", json=json_data
            )
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            self.logger.error(f"Failed to {operation_name}: {e}")
            return None

    def create_session(
        self, player_name: str, earned: float = 0.0, spent: float = 0.0
    ) -> Optional[Session]:
        """Create a new game session."""
        session_id = str(uuid.uuid4())
        session_data = SessionCreate(
            player_name=player_name,
            session_id=session_id,
            earned=earned,
            spent=spent,
            net_income=earned - spent,
        )

        response_data = self._make_request(
            "POST", "/sessions/", "create session", session_data.dict()
        )
        return Session(**response_data) if response_data else None

    def update_session(
        self, session_id: str, earned: float, spent: float
    ) -> Optional[Session]:
        """Update an existing session with final scores."""
        session_update = SessionUpdate(
            earned=earned, spent=spent, net_income=earned - spent
        )

        response_data = self._make_request(
            "PUT",
            f"/sessions/{session_id}",
            "update session",
            session_update.dict(exclude_unset=True),
        )
        return Session(**response_data) if response_data else None

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by session ID."""
        response_data = self._make_request(
            "GET", f"/sessions/{session_id}", "get session"
        )
        return Session(**response_data) if response_data else None

    def get_sessions_by_player(self, player_name: str) -> list[Session]:
        """Get all sessions for a specific player."""
        response_data = self._make_request(
            "GET", f"/sessions/player/{player_name}", "get sessions for player"
        )
        return (
            [Session(**session) for session in response_data] if response_data else []
        )

    def get_leaderboard(self, limit: int = 10) -> list[Session]:
        """Get the leaderboard with top scores."""
        response_data = self._make_request(
            "GET", f"/leaderboard/?limit={limit}", "get leaderboard"
        )
        return (
            [Session(**session) for session in response_data] if response_data else []
        )

    def get_player_best_score(self, player_name: str) -> Optional[Session]:
        """Get the best score for a specific player."""
        response_data = self._make_request(
            "GET", f"/leaderboard/player/{player_name}", "get player best score"
        )
        return Session(**response_data) if response_data else None
