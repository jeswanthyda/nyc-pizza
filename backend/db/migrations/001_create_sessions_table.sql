-- Migration: Create sessions table
-- Created: 2024-01-01
-- Description: Creates the sessions table for storing game session data

CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR PRIMARY KEY,
    player_name VARCHAR NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    earned REAL DEFAULT 0.0 NOT NULL,
    spent REAL DEFAULT 0.0 NOT NULL,
    net_income REAL DEFAULT 0.0 NOT NULL
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sessions_session_id ON sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_sessions_player_name ON sessions(player_name);
CREATE INDEX IF NOT EXISTS idx_sessions_timestamp ON sessions(timestamp);
