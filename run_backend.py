#!/usr/bin/env python3
"""
Script to run the FastAPI server
"""

import uvicorn

from backend.logging_utils import get_logger

# Initialize logging
logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting NYC Pizza FastAPI server...")
    uvicorn.run(
        "backend.server.fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info",
        access_log=True,
    )
