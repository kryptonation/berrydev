# app/schemas.py

from pydantic import BaseModel


class WebHookData(BaseModel):
    """
    Pydantic model for validating the webhook data
    """
    source: str
    data: dict


class TaskCancel(BaseModel):
    """
    Pydantic model for validating the task cancel request
    """
    task_id: str