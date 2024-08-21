# app/auth.py

from fastapi import Depends, HTTPException, Header
from app.config import settings
import logging

# Initialize the logger
logger = logging.getLogger(__name__)

def verify_api_key(x_api_key: str = Header(...)):
    """
    Verify the API key in the request header

    Args:
        x_api_key (str): API key in the request header

    Raises:
        HTTPException: If the API key is invalid
    """
    if x_api_key != settings.api_key:
        logger.error(f"Invalid API key: {x_api_key}")
        raise HTTPException(status_code=403, detail="Invalid API Key")