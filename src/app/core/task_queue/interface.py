"""Task queue interface. Use this to enqueue background tasks from any layer."""

from typing import Any

import redis.asyncio as aioredis
from saq import Queue

from app.core.config import get_settings
from app.worker.config import QUEUE_NAME

_queue: Queue | None = None


async def get_queue() -> Queue:
    """Get or create the SAQ queue instance."""
    global _queue  # noqa: PLW0603 - module-level singleton by design
    if _queue is None:
        settings = get_settings()
        r = aioredis.from_url(settings.redis_url)
        _queue = Queue(r, name=QUEUE_NAME)
    return _queue


async def enqueue(task_name: str, *, timeout: int, **kwargs: Any) -> str:
    """Enqueue a task by name.

    IMPORTANT: Always specify timeout explicitly. SAQ defaults to 10 seconds
    which is far too short for I/O or LLM calls. Use DEFAULT_JOB_TIMEOUT (300s)
    from app.worker.config.

    Args:
        task_name: Name of the task (must be registered in ALL_TASKS)
        timeout: Job timeout in seconds (required, no default — forces explicit choice)
        **kwargs: Arguments passed to the task function

    Returns:
        Job ID
    """
    queue = await get_queue()
    job = await queue.enqueue(task_name, timeout=timeout, **kwargs)
    return job.id
