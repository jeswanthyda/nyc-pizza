import sqlite3
from typing import List

from backend.db.connection import get_db_dependency
from backend.server.crud import SessionsCRUD
from backend.server.schemas import SessionCreate, SessionResponse, SessionUpdate
from fastapi import Depends, FastAPI, HTTPException, status

# Create FastAPI app
app = FastAPI(
    title="NYC Pizza Game API",
    description="API for managing game sessions",
    version="1.0.0",
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "NYC Pizza Game API is running!"}


@app.post(
    "/sessions/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_session(
    session: SessionCreate, db: sqlite3.Connection = Depends(get_db_dependency)
):
    """Create a new game session"""
    try:
        crud = SessionsCRUD(db)
        # Check if session_id already exists
        existing_session = crud.get_session_by_session_id(session.session_id)
        if existing_session:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session ID already exists",
            )

        return crud.create_session(session)
    except Exception as e:
        print(f"Error in create_new_session: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@app.get("/sessions/", response_model=List[SessionResponse])
async def read_sessions(
    skip: int = 0, limit: int = 100, db: sqlite3.Connection = Depends(get_db_dependency)
):
    """Get all sessions with pagination"""
    crud = SessionsCRUD(db)
    sessions = crud.get_all_sessions(skip=skip, limit=limit)
    return sessions


@app.get("/sessions/{session_id}", response_model=SessionResponse)
async def read_session(
    session_id: str, db: sqlite3.Connection = Depends(get_db_dependency)
):
    """Get a specific session by session_id"""
    crud = SessionsCRUD(db)
    session = crud.get_session_by_session_id(session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return session


@app.get("/sessions/player/{player_name}", response_model=List[SessionResponse])
async def read_sessions_by_player(
    player_name: str, db: sqlite3.Connection = Depends(get_db_dependency)
):
    """Get all sessions for a specific player"""
    crud = SessionsCRUD(db)
    sessions = crud.get_sessions_by_player_name(player_name)
    return sessions


@app.put("/sessions/{session_id}", response_model=SessionResponse)
async def update_existing_session(
    session_id: str,
    session_update: SessionUpdate,
    db: sqlite3.Connection = Depends(get_db_dependency),
):
    """Update an existing session"""
    crud = SessionsCRUD(db)
    session = crud.update_session(session_id, session_update)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return session


@app.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_session(
    session_id: str, db: sqlite3.Connection = Depends(get_db_dependency)
):
    """Delete a session"""
    crud = SessionsCRUD(db)
    success = crud.delete_session(session_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
