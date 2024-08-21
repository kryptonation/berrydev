# app/tests/test_api.py

import pytest
import asyncio
from app.tasks import tasks

# Test cases for the POST /webhook endpoint
def test_webhook_valid_source_crm(client):
    response = client.post("/api/v1/webhook", json={"source": "crm", "data": {}})
    assert response.status_code == 200
    assert response.json() == {"status": "Synchronization initialized"}

def test_webhook_valid_source_marketing(client):
    response = client.post("/api/v1/webhook", json={"source": "marketing", "data": {}})
    assert response.status_code == 200
    assert response.json() == {"status": "Synchronization initialized"}

def test_webhook_invalid_source(client):
    response = client.post("/api/v1/webhook", json={"source": "invalid_source", "data": {}})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid data source"}

# Test cases for the GET /data endpoint
def test_get_data_default_pagination(client):
    response = client.get("/api/v1/data")
    assert response.status_code == 200
    assert "customers" in response.json()
    assert "campaigns" in response.json()

def test_get_data_with_pagination(client):
    response = client.get("/api/v1/data", params={"offset": 0, "limit": 5})
    assert response.status_code == 200
    assert "customers" in response.json()
    assert "campaigns" in response.json()

# Test cases for the GET /sync/{source} endpoint
def test_sync_valid_source_crm(client):
    response = client.get("/api/v1/sync/crm")
    assert response.status_code == 200
    assert response.json() == {"status": "sync started"}

def test_sync_valid_source_marketing(client):
    response = client.get("/api/v1/sync/marketing")
    assert response.status_code == 200
    assert response.json() == {"status": "sync started"}

def test_sync_invalid_source(client):
    response = client.get("/api/v1/sync/invalid_source")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid source"}

# Test cases for the GET /tasks endpoint
def test_list_tasks_no_running_tasks(client):
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert response.json() == {"tasks": []}

@pytest.mark.asyncio
async def test_list_tasks_with_running_tasks(client, clear_tasks_before_each_test):
    # Simulate a running task
    task_id = "test-task"
    tasks[task_id] = asyncio.create_task(asyncio.sleep(10))  # Add a dummy task for testing
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert response.json() == {"tasks": [task_id]}

# Test cases for the POST /tasks/cancel endpoint
@pytest.mark.asyncio
async def test_cancel_existing_task(client, clear_tasks_before_each_test):

    task_id = "test-task"
    tasks[task_id] = asyncio.create_task(asyncio.sleep(10))   # Add a dummy task for testing
    response = client.post("/api/v1/tasks/cancel", json={"task_id": task_id})
    assert response.status_code == 200
    assert response.json() == {"status": "task cancelled"}

def test_cancel_nonexistent_task(client, clear_tasks_before_each_test):
    response = client.post("/api/v1/tasks/cancel", json={"task_id": "nonexistent-task"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


@pytest.fixture(autouse=True)
def clear_tasks_before_each_test():
    global tasks
    tasks.clear()  # Clear tasks before each test runs