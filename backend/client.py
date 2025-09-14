"""FastAPI client for logging game sessions to the database."""

import uuid
from typing import Optional

import httpx

from .server.schemas import SessionCreate, SessionResponse, SessionUpdate


class FastAPIClient:
    """Client for communicating with the FastAPI server."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the client with the server base URL."""
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=10.0)

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

    def create_session(
        self, player_name: str, earned: float = 0.0, spent: float = 0.0
    ) -> Optional[SessionResponse]:
        """Create a new game session."""
        session_id = str(uuid.uuid4())
        session_data = SessionCreate(
            player_name=player_name,
            session_id=session_id,
            earned=earned,
            spent=spent,
            net_income=earned - spent,
        )

        try:
            response = self.client.post(
                f"{self.base_url}/sessions/", json=session_data.dict()
            )
            response.raise_for_status()
            return SessionResponse(**response.json())
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Failed to create session: {e}")
            return None

    def update_session(
        self, session_id: str, earned: float, spent: float
    ) -> Optional[SessionResponse]:
        """Update an existing session with final scores."""
        session_update = SessionUpdate(
            earned=earned, spent=spent, net_income=earned - spent
        )

        try:
            response = self.client.put(
                f"{self.base_url}/sessions/{session_id}",
                json=session_update.dict(exclude_unset=True),
            )
            response.raise_for_status()
            return SessionResponse(**response.json())
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Failed to update session: {e}")
            return None

    def get_session(self, session_id: str) -> Optional[SessionResponse]:
        """Get a session by session ID."""
        try:
            response = self.client.get(f"{self.base_url}/sessions/{session_id}")
            response.raise_for_status()
            return SessionResponse(**response.json())
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Failed to get session: {e}")
            return None

    def get_sessions_by_player(self, player_name: str) -> list[SessionResponse]:
        """Get all sessions for a specific player."""
        try:
            response = self.client.get(f"{self.base_url}/sessions/player/{player_name}")
            response.raise_for_status()
            return [SessionResponse(**session) for session in response.json()]
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Failed to get sessions for player: {e}")
            return []
