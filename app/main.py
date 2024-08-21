# app/main.py

import logging
import asyncio
import uuid
from typing import List
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks, Request
from jinja2 import Template
from fastapi.responses import HTMLResponse
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

tasks = {}  # Global dictionary to store tasks
clients: List[WebSocket] = []  # List of connected WebSocket clients

tasks = {}  # Global dictionary to store tasks
clients: List[WebSocket] = []  # List of connected WebSocket clients

# Function to simulate a long-running task
async def long_running_task(task_id: str, duration: int):
    try:
        for i in range(duration):
            await asyncio.sleep(1)  # Simulate work by sleeping
            # Optionally, send progress updates
        tasks[task_id]['status'] = 'completed'
    except asyncio.CancelledError:
        tasks[task_id]['status'] = 'cancelled'
        raise
    finally:
        update_clients()

# Function to update all clients with the latest task information
def update_clients():
    data = {"tasks": [{"task_id": task_id, "status": tasks[task_id]['status']} for task_id in tasks.keys()]}
    for client in clients:
        asyncio.create_task(client.send_json(data))

# Serve the enhanced dashboard HTML with Tailwind CSS and WebSocket support
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 text-gray-800">
        <div class="container mx-auto p-4">
            <h1 class="text-3xl font-bold mb-4">Task Dashboard</h1>
            <div id="task-container" class="space-y-4">
                {% for task in running_tasks %}
                    <div class="bg-white p-4 shadow rounded task" id="task-{{ task.task_id }}">
                        <span>Task ID: {{ task.task_id }} ({{ task.status }})</span>
                        <button class="bg-red-500 text-white py-1 px-2 rounded ml-4" onclick="cancelTask('{{ task.task_id }}')">Cancel</button>
                    </div>
                {% endfor %}
            </div>
            <div class="mt-6">
                <h2 class="text-xl font-semibold">Add New Task</h2>
                <input type="number" id="task-duration" placeholder="Duration in seconds" class="border border-gray-300 p-2 rounded">
                <button class="bg-blue-500 text-white py-1 px-4 rounded" onclick="addTask()">Add Task</button>
            </div>
        </div>
        <script>
            const ws = new WebSocket(`ws://${location.host}/ws`);

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                const taskContainer = document.getElementById('task-container');
                taskContainer.innerHTML = '';

                data.tasks.forEach(task => {
                    const taskDiv = document.createElement('div');
                    taskDiv.className = 'bg-white p-4 shadow rounded task';
                    taskDiv.id = 'task-' + task.task_id;

                    taskDiv.innerHTML = `
                        <span>Task ID: ${task.task_id} (${task.status})</span>
                        <button class="bg-red-500 text-white py-1 px-2 rounded ml-4" onclick="cancelTask('${task.task_id}')">Cancel</button>
                    `;

                    taskContainer.appendChild(taskDiv);
                });
            };

            async function addTask() {
                const duration = document.getElementById('task-duration').value;
                const response = await fetch(`/tasks/add?duration=${duration}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ duration: duration })
                });
                if (response.ok) {
                    alert('Task added.');
                    document.getElementById('task-duration').value = '';
                } else {
                    alert('Failed to add task.');
                }
            }

            async function cancelTask(task_id) {
                const response = await fetch('/tasks/cancel', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task_id: task_id })
                });
                if (response.ok) {
                    alert('Task ' + task_id + ' cancelled.');
                } else {
                    alert('Failed to cancel task ' + task_id);
                }
            }
        </script>
    </body>
    </html>
    """)

    running_tasks = [{"task_id": task_id, "status": tasks[task_id]['status']} for task_id in tasks.keys()]
    html_content = template.render(running_tasks=running_tasks)
    return HTMLResponse(content=html_content)

# WebSocket endpoint to send real-time task updates to clients
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection open
    except WebSocketDisconnect:
        clients.remove(websocket)

# Endpoint to add a new task
@app.post("/tasks/add")
async def add_task(background_tasks: BackgroundTasks, duration: int):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "task": background_tasks.add_task(long_running_task, task_id, duration),
        "status": "running"
    }
    update_clients()
    return {"task_id": task_id, "status": "running"}

# Endpoint to cancel a specific task
@app.post("/tasks/cancel")
async def cancel_task(task: dict):
    task_id = task.get("task_id")
    if task_id not in tasks:
        return {"status": "task not found"}, 404

    task_to_cancel = tasks[task_id].get("task")
    if task_to_cancel is None:
        return {"status": "task cannot be cancelled, not found or already completed"}, 400

    task_to_cancel.cancel()  # This will raise an exception if the task is None
    tasks[task_id]['status'] = 'cancelled'
    update_clients()
    return {"status": "task cancelled"}