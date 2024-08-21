# app/api.py

import logging
from app.utils import fetch_data_from_source
from app.models import Customer, Campaign
from app.db import SessionLocal
from app.config import settings

# Initialize the logger
logger = logging.getLogger(__name__)

async def sync_sources_data(source: str):
    """
    Synchronize the data from the external API source to the database

    Args:
        source (str): Data source to sync data from (eg: 'crm', 'marketing')
    """
    db = SessionLocal()
    try:
        if source == "crm":
            data = await fetch_data_from_source(settings.crm_api_url, {"limit": 100})
            for customer in data.get("results", []):
                db.add(Customer(**customer))
                logger.info(f"Added customer {customer['id']} to the database")
        elif source == "marketing":
            data = await fetch_data_from_source(settings.marketing_api_url, {"limit": 100})
            for campaign in data.get("results", []):
                db.add(Campaign(**campaign))
                logger.info(f"Added campaign {campaign['id']} to the database")
        db.commit()
    except Exception as e:
        logger.error(f"Error syncing data from {source}: {e}")
    finally:
        db.close()
    