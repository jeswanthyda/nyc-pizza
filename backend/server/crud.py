import sqlite3
from typing import List, Optional

from ..db.models import Session
from .schemas import SessionCreate, SessionUpdate


class SessionsCRUD:
    """CRUD operations for sessions"""

    def __init__(self, db: sqlite3.Connection):
        """Initialize with database connection"""
        self.db = db

    def create_session(self, session: SessionCreate) -> Session:
        """Create a new session"""
        session_data = session.model_dump()

        # Insert the session
        _ = self.db.execute(
            """
            INSERT INTO sessions (player_name, session_id, earned, spent, net_income)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                session_data["player_name"],
                session_data["session_id"],
                session_data["earned"],
                session_data["spent"],
                session_data["net_income"],
            ),
        )
        self.db.commit()

        # Get the created session
        created_session = self.get_session_by_session_id(session_data["session_id"])
        if created_session is None:
            raise RuntimeError("Failed to create session")
        return created_session

    def get_session_by_session_id(self, session_id: str) -> Optional[Session]:
        """Get a session by id"""
        cursor = self.db.execute(
            "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
        )
        row = cursor.fetchone()

        if row:
            return Session.from_row(row)
        return None

    def update_session(
        self, session_id: str, session_update: SessionUpdate
    ) -> Optional[Session]:
        """Update a session"""
        update_data = session_update.model_dump(exclude_unset=True)

        if not update_data:
            return self.get_session_by_session_id(session_id)

        # Build dynamic update query
        set_clauses = [f"{field} = ?" for field in update_data.keys()]
        params = list(update_data.values()) + [session_id]

        query = f"""
            UPDATE sessions 
            SET {", ".join(set_clauses)}
            WHERE session_id = ?
        """

        self.db.execute(query, params)
        self.db.commit()

        return self.get_session_by_session_id(session_id)

    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        cursor = self.db.execute(
            "DELETE FROM sessions WHERE session_id = ?", (session_id,)
        )
        self.db.commit()
        return cursor.rowcount > 0

    def get_all_sessions(self, skip: int = 0, limit: int = 100) -> List[Session]:
        """Get all sessions with pagination"""
        cursor = self.db.execute(
            "SELECT * FROM sessions ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            (limit, skip),
        )
        rows = cursor.fetchall()
        return [Session.from_row(row) for row in rows]

    def get_sessions_by_player_name(self, player_name: str) -> List[Session]:
        """Get all sessions for a specific player"""
        cursor = self.db.execute(
            "SELECT * FROM sessions WHERE player_name = ? ORDER BY timestamp DESC",
            (player_name,),
        )
        rows = cursor.fetchall()
        return [Session.from_row(row) for row in rows]
