from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Session(BaseModel):
    """Session model for game sessions"""

    player_name: str = ""
    session_id: str = ""
    timestamp: Optional[datetime] = None
    earned: float = 0.0
    spent: float = 0.0
    net_income: float = 0.0

    class Config:
        from_attributes = True

    def __repr__(self):
        return f"<Session(player_name='{self.player_name}', session_id='{self.session_id}', net_income={self.net_income})>"

    @classmethod
    def from_row(cls, row) -> "Session":
        """Create a Session instance from a database row"""
        return cls(
            player_name=row["player_name"],
            session_id=row["session_id"],
            timestamp=datetime.fromisoformat(row["timestamp"])
            if row["timestamp"]
            else None,
            earned=row["earned"],
            spent=row["spent"],
            net_income=row["net_income"],
        )
