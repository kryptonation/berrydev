# app/endpoints.py

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Customer, Campaign
from app.schemas import WebHookData, TaskCancel
from app.db import get_db
from app.tasks import init_background_task, cancel_task, get_tasks_list

# Initialize the logger
logger = logging.getLogger(__name__)

# Initialize the API router
router = APIRouter()

@router.post("/webhook")
async def webhook(data: WebHookData):
    """
    Endpoint to receive webhook data from the external API source

    Args:
        data (WebHookData): Data received from the webhook

    Returns:
        dict: Status of the sync operation
    """
    if data.source not in ["crm", "marketing"]:
        logger.error(f"Invalid data source: {data.source}")
        raise HTTPException(status_code=400, detail="Invalid data source")
    
    await init_background_task(data.source)
    logging.info(f"Received webhook data from {data.source}")
    return {"status": "Synchronization initialized"}


@router.get("/data")
async def get_data(offset: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve stored data with pagination.

    Args:
        offset (int): The offset for pagination.
        limit (int): The limit for pagination.
        db (Session): The database session dependency.

    Returns:
        dict: The retrieved customers and campaigns.
    """
    customers = db.query(Customer).offset(offset).limit(limit).all()
    campaigns = db.query(Campaign).offset(offset).limit(limit).all()
    logging.info(f"Retrieved data with offset {offset} and limit {limit}")
    return {"customers": customers, "campaigns": campaigns}


@router.get("/sync/{source}")
async def sync_source(source: str):
    """
    Endpoint to trigger data synchronization from a specific source.

    Args:
        source (str): The data source to sync from (e.g., "crm", "marketing").

    Returns:
        dict: Status of the sync operation.
    """
    if source not in ["crm", "marketing"]:
        logging.error(f"Invalid source provided: {source}")
        raise HTTPException(status_code=400, detail="Invalid source")
    
    await init_background_task(source)
    logging.info(f"Sync started for source: {source}")
    return {"status": "sync started"}


@router.get("/tasks")
async def list_tasks():
    """
    Endpoint to list all running background tasks.

    Returns:
        dict: List of running tasks.
    """
    running_tasks = get_tasks_list()
    logging.info(f"Listing running tasks: {running_tasks}")
    return {"tasks": running_tasks}


@router.post("/tasks/cancel")
async def cancel_background_task(task_cancel: TaskCancel):
    """
    Endpoint to cancel a specific background task.

    Args:
        task_cancel (schemas.TaskCancel): The task cancellation request.

    Returns:
        dict: Status of the cancellation operation.
    """
    if cancel_task(task_cancel.task_id):
        logging.info(f"Task {task_cancel.task_id} cancelled successfully")
        return {"status": "task cancelled"}
    else:
        logging.error(f"Task {task_cancel.task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")