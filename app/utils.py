# app/utils.py

import httpx
import logging
from app.config import settings

# Initialize the logger
logger = logging.getLogger(__name__)

async def fetch_data_from_source(source: str, params: dict) -> dict:
    """
    Fetch data from the external source API

    Args:
        source (str): Data source to fetch data from (eg: 'crm', 'marketing')
    Returns:
        dict: Data fetched from the source API
    """
    headers = {"X-API-KEY": settings.api_key}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.api_url}/{source}", headers=headers, params=params)
            response.raise_for_status()
            logger.info(f"Fetched data from {source}")
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to fetch data from {source}. {e}")
        return {}