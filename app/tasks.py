# app/tasks.py

import asyncio
import logging
from typing import Dict

from app.api import sync_sources_data

# Initialize the logger
logger = logging.getLogger(__name__)

# Initialize the dictionary to track background tasks
tasks: Dict[str, asyncio.Task] = {}

async def init_background_task(source: str):
    """
    Create and init background task to sync data from source

    Args:
        source (str): Data source to sync data from (eg: 'crm', 'marketing')
    """
    task = asyncio.create_task(sync_sources_data(source))
    tasks[task.get_name()] = task
    logger.info(f"Background task {task.get_name()} started")
    await task


def cancel_task(task_id: str):
    """
    Cancel the background task

    Args:
        task_id (str): Task ID to cancel
    Returns:
        bool: True if task is cancelled, False if task not found
    """
    task = tasks.get(task_id)
    if task:
        task.cancel()
        logger.info(f"Background task {task.get_name()} cancelled")
        return True
    else:
        logger.error(f"Task with ID {task_id} not found")
        return False
    

def get_tasks_list() -> list:
    """
    Get the list of running background tasks

    Returns:
        list: List of running background tasks
    """
    return [tasks.keys()]
