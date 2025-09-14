import os
import sqlite3
from typing import Generator

# SQLite database path - use absolute path to avoid issues when running from different directories
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "nyc_pizza.db")


def get_db_connection() -> sqlite3.Connection:
    """Get a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn


def get_db_dependency() -> Generator[sqlite3.Connection, None, None]:
    """FastAPI dependency that provides a database connection with automatic cleanup"""
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()
