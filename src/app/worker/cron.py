"""Cron job definitions for scheduled background work."""

from saq import CronJob

# Add cron jobs here. Example:
# CronJob(function=my_task, cron="0 * * * *", timeout=300)

CRON_JOBS: list[CronJob] = []
