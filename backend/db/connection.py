import os
import sqlite3
from contextlib import contextmanager
from typing import Generator

# SQLite database path - use absolute path to avoid issues when running from different directories
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "nyc_pizza.db")


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False, timeout=30.0)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_db_dependency() -> Generator[sqlite3.Connection, None, None]:
    """FastAPI dependency that provides a fresh database connection per request."""
    with get_db_connection() as conn:
        yield conn
