"""SAQ worker settings. Entry point: saq app.worker.settings"""

from app.core.config import get_settings
from app.worker.config import QUEUE_NAME
from app.worker.tasks import ALL_TASKS
from app.worker.cron import CRON_JOBS

settings_obj = get_settings()

settings = {
    "queue": {
        "name": QUEUE_NAME,
        "url": settings_obj.redis_url,
    },
    "functions": list(ALL_TASKS.values()),
    "cron_jobs": CRON_JOBS,
    "concurrency": 10,
}
