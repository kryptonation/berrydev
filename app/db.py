# app/db.py

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


# Create the engine for the database connection
engine = create_engine(settings.database_url)

# Create a factory session object for the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for the database models
Base = declarative_base()
metadata = MetaData()

# Create a function to get the database session
def get_db():
    """
    Dependency to get the database session
    This will be used by endpoints to get the database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()