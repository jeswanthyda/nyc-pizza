import os
import sqlite3
from contextlib import contextmanager
from typing import Generator

# SQLite database path - use absolute path to avoid issues when running from different directories
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "nyc_pizza.db")


def get_db_connection() -> sqlite3.Connection:
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections"""
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


def get_db_dependency() -> sqlite3.Connection:
    """FastAPI dependency that returns a database connection"""
    return get_db_connection()
