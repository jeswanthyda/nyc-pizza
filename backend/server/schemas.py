from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SessionBase(BaseModel):
    player_name: str
    session_id: str
    earned: float = 0.0
    spent: float = 0.0
    net_income: float = 0.0


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    player_name: Optional[str] = None
    earned: Optional[float] = None
    spent: Optional[float] = None
    net_income: Optional[float] = None


class SessionResponse(SessionBase):
    timestamp: datetime

    class Config:
        from_attributes = True
