
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
- **POST /tasks/add:** Adds a new task. Requires a `duration` parameter (in seconds).
- **POST /tasks/cancel:** Cancels an existing task. Requires a `task_id` parameter.
- **GET /tasks/status:** Returns the status of all tasks.
- **WebSocket /ws:** WebSocket endpoint for real-time task updates.

## Usage

1. **Adding a Task:**
   - Enter the duration (in seconds) in the provided input field and click "Add Task".
   - The task will start running, and its status will be displayed on the dashboard.

2. **Canceling a Task:**
   - Click the "Cancel" button next to a running task to stop it.
   - The dashboard will update in real-time to reflect the cancellation.

3. **Monitoring Task Status:**
   - The dashboard automatically updates the status of all tasks in real-time.

## Real-time Updates

This application uses WebSockets to provide real-time updates to all connected clients. Whenever a task is added, updated, or canceled, all clients are immediately notified, and their dashboards are refreshed.

## Tailwind CSS

The application is styled using Tailwind CSS, which is included via a CDN link. This makes the interface responsive and modern, with minimal custom CSS required.

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
