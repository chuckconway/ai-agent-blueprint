"""Example tool demonstrating the @tool registration pattern."""

from datetime import datetime, timezone

from app.agent.tools import tool


@tool("get_current_time", "Get the current date and time in UTC")
async def get_current_time() -> str:
    """Return the current UTC time as a formatted string."""
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S UTC")
