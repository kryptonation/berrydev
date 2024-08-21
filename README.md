
# FastAPI Task Dashboard

This project is a FastAPI application that serves as a task management dashboard. It allows users to add long-running tasks, monitor their status, and cancel them through a web-based interface. The dashboard provides real-time updates using WebSockets and is styled with Tailwind CSS.

## Features

- **Real-time Dashboard:** The dashboard displays the status of all running tasks in real-time using WebSockets.
- **Task Management:** Add, monitor, and cancel tasks via the dashboard.
- **Responsive Design:** The interface is styled with Tailwind CSS for a modern, responsive look.
- **WebSocket Integration:** Clients receive updates on task status in real-time without needing to refresh the page.

## Prerequisites

- Python 3.8+
- FastAPI
- Uvicorn (ASGI server)

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fastapi-task-dashboard
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the dashboard:**
   Open your web browser and navigate to `http://localhost:8000/dashboard` to view the task dashboard.

## API Endpoints

- **GET /dashboard:** Returns the HTML for the task dashboard.
- **POST /tasks/add:** Adds a new task. Requires a JSON body with `duration` parameter (in seconds).
- **POST /tasks/cancel:** Cancels an existing task. Requires a JSON body with `task_id` parameter.
- **GET /tasks/status:** Returns the status of all tasks.
- **WebSocket /ws:** WebSocket endpoint for real-time task updates.

### Example of Adding a Task

To add a task with a duration of 10 seconds:

```bash
curl -X POST "http://localhost:8000/tasks/add" -H "Content-Type: application/json" -d '{"duration": 10}'
```

### Example of Canceling a Task

To cancel a task with a specific `task_id`:

```bash
curl -X POST "http://localhost:8000/tasks/cancel" -H "Content-Type: application/json" -d '{"task_id": "your-task-id"}'
```

## Data Modeling Decisions

The application uses a simple in-memory data structure (a Python dictionary) to store tasks. Each task is assigned a unique ID, and the dictionary stores the task's status and reference to the `asyncio.Task` object. This allows the application to manage tasks efficiently without needing a persistent database for this use case.

## Background Task Management

Background tasks are managed using Python's `asyncio` library. Each task is created using `asyncio.create_task()` and is tracked in a global dictionary. This allows the application to perform long-running tasks asynchronously, providing non-blocking task management.

### Key Considerations:
- **Task Creation:** Tasks are created asynchronously to avoid blocking the main application thread.
- **Task Cancellation:** Tasks can be canceled using the `cancel()` method provided by `asyncio`. The status of canceled tasks is updated accordingly.
- **Real-Time Updates:** The dashboard is updated in real-time using WebSockets, allowing users to see the status of tasks without refreshing the page.

## Troubleshooting Common Issues

### Missing `duration` Parameter in /tasks/add

If you encounter an error like `{"detail": [{"loc": ["query", "duration"], "msg": "Field required"}]`, ensure that you are sending the `duration` parameter in the JSON body of the POST request.

### Cancel Task Error

If you see an error like `AttributeError: 'NoneType' object has no attribute 'cancel'` when canceling a task, it indicates that the task might not be properly initialized. Ensure that tasks are correctly created and stored in the global `tasks` dictionary.

## Usage of AI in Building the Project

While AI was not directly used in the execution of this project, AI tools were utilized for:
- **Code Suggestions:** AI-assisted coding tools helped streamline the development process by providing quick recommendations and ensuring best practices.
- **Debugging:** AI-assisted tools were used to analyze errors and provide guidance on fixing issues efficiently.

## Future Enhancements

- **Task Progress Tracking:** Add a progress bar to visually display task completion.
- **User Authentication:** Implement user login and access control for the dashboard.
- **Advanced Task Management:** Include features like task prioritization and scheduling.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## Contact

For any questions or feedback, please contact [your email or GitHub profile].
