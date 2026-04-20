"""Example background task demonstrating SAQ task patterns."""

import structlog

logger = structlog.get_logger()


async def example_task(ctx: dict, *, name: str = "world") -> str:
    """Example task that logs a greeting.

    This demonstrates the basic SAQ task pattern:
    - ctx dict is provided by SAQ (contains job info)
    - Keyword arguments are passed when enqueueing
    - Always use explicit timeout when enqueueing (see worker/config.py)

    Usage:
        from app.core.task_queue import enqueue
        from app.worker.config import DEFAULT_JOB_TIMEOUT
        await enqueue("example_task", timeout=DEFAULT_JOB_TIMEOUT, name="Blueprint")
    """
    logger.info("example_task_started", name=name)
    message = f"Hello, {name}!"
    logger.info("example_task_completed", message=message)
    return message
