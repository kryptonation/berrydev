# app/tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, get_db

# Configure test database
TEST_DATABASE_URL = "sqlite:///testdb.sqlite3"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Fixture to provide a test client for making API requests
@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)  # Create tables
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)  # Drop tables after tests
