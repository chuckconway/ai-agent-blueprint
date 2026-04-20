"""SAQ worker configuration and constants."""

# Default timeout for all jobs (5 minutes).
# SAQ defaults to 10 seconds which is far too short for any I/O or LLM call.
DEFAULT_JOB_TIMEOUT = 300

QUEUE_NAME = "default"
