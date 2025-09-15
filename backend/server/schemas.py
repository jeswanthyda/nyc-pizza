from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from backend.db.models import Session


class SessionCreate(Session):
    """Schema for creating a new session"""

    # Inherit all fields from Session but make timestamp optional for creation
    timestamp: Optional[datetime] = None


class SessionUpdate(BaseModel):
    """Schema for updating a session"""

    # All fields optional for updates
    player_name: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    earned: Optional[float] = None
    spent: Optional[float] = None
    net_income: Optional[float] = None
