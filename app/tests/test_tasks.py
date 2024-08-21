# app/tests/test_tasks.py

import pytest
import asyncio

from app.tasks import init_background_task, cancel_task, get_tasks_list, tasks

@pytest.mark.asyncio
async def test_init_background_task_invalid_source():
    with pytest.raises(ValueError):
        await init_background_task("invalid_source")

@pytest.mark.asyncio
async def test_cancel_task_existing_task(clear_tasks_before_each_test):
    task_id = "test-task"
    tasks[task_id] = asyncio.create_task(asyncio.sleep(1))
    assert cancel_task(task_id) is True
    assert task_id not in tasks

def test_cancel_task_nonexistent_task(clear_tasks_before_each_test):
    assert cancel_task("nonexistent-task") is False

def test_get_tasks_list(clear_tasks_before_each_test):
    task_id = "test-task"
    tasks[task_id] = None  # Add a dummy task for testing
    running_tasks = get_tasks_list()
    assert task_id in running_tasks
    del tasks[task_id]  # Clean up after test

@pytest.fixture(autouse=True)
def clear_tasks_before_each_test():
    global tasks
    tasks.clear()  # Clear tasks before each test runs