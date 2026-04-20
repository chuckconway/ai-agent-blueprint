"""Task registry. Import all task functions and register them in ALL_TASKS."""

from app.worker.tasks.example import example_task

# Map of task_name -> task_function
# Add new tasks here as they are created
ALL_TASKS: dict[str, object] = {
    "example_task": example_task,
}
