# app/main.py

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.endpoints import router

# Initialize the logger
logger = logging.getLogger(__name__)

# Initialize the FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_hosts.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(router, prefix="/api/v1")