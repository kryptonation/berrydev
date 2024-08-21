# app/models.py

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, JSON, DateTime

from app.db import Base


class Customer(Base):
    """
    ORM model to store the customer information from crm api
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(tz=timezone.utc))


class Campaign(Base):
    """
    ORM model to store the campaign information from marketing api
    """
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(tz=timezone.utc))