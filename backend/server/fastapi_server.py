import sqlite3
from typing import List

from backend.db.connection import get_db_dependency
from backend.db.models import Session
from backend.logging_utils import get_logger
from backend.server.schemas import SessionCreate, SessionUpdate
from backend.server.sessions_handler import SessionsHandler
from fastapi import Depends, FastAPI, HTTPException, status

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="NYC Pizza Game API",
    description="API for managing game sessions",
    version="1.0.0",
)


@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("Root endpoint accessed")
    return {"message": "NYC Pizza Game API is running!"}


@app.post("/sessions/", response_model=Session, status_code=status.HTTP_201_CREATED)
async def create_new_session(
    session: SessionCreate, db: sqlite3.Connection = Depends(get_db_dependency)
):
    """Create a new game session"""
    logger.info(
        f"Creating new session for player: {session.player_name}, session_id: {session.session_id}"
    )
    try:
        handler = SessionsHandler(db)
        # Check if session_id already exists
        existing_session = handler.get_session_by_id(session.session_id)
        if existing_session:
            logger.warning(f"Session ID already exists: {session.session_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session ID already exists",
            )

        created_session = handler.create_session(session)
        logger.info(f"Successfully created session: {session.session_id}")
        return created_session
    except Exception as e:
        logger.error(f"Error in create_new_session: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@app.get("/sessions/", response_model=List[Session])
async def read_sessions(
    skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db_dependency)
):
    """Get all sessions with pagination"""
    handler = SessionsHandler(db)
    sessions = handler.get_all_sessions(skip=skip, limit=limit)
    return sessions


@app.get("/sessions/{session_id}", response_model=Session)
async def read_session(
    session_id: str, db: sqlite3.Connection = Depends(get_db_dependency)
):
    """Get a specific session by session_id"""
    logger.info(f"Retrieving session: {session_id}")
    handler = SessionsHandler(db)
    session = handler.get_session_by_id(session_id)
    if session is None:
        logger.warning(f"Session not found: {session_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return session


@app.get("/sessions/player/{player_name}", response_model=List[Session])
async def read_sessions_by_player(
    player_name: str, db: sqlite3.Connection = Depends(get_db_dependency)
):
    """Get all sessions for a specific player"""
    handler = SessionsHandler(db)
    sessions = handler.get_sessions_by_player_name(player_name)
    return sessions


@app.put("/sessions/{session_id}", response_model=Session)
async def update_existing_session(
    session_id: str,
    session_update: SessionUpdate,
    db: sqlite3.Connection = Depends(get_db_dependency),
):
    """Update an existing session"""
    logger.info(f"Updating session: {session_id}")
    handler = SessionsHandler(db)
    session = handler.update_session(session_id, session_update)
    if session is None:
        logger.warning(f"Session not found for update: {session_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    logger.info(f"Successfully updated session: {session_id}")
    return session


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
