"""SSE streaming utilities for the agent layer."""

import json
from dataclasses import dataclass
from typing import Any, AsyncIterator

from starlette.responses import StreamingResponse


@dataclass
class StreamEvent:
    """A server-sent event emitted during agent execution.

    Event types: text_delta, tool_call_started, tool_call_completed, done, error.
    """

    event: str
    data: dict[str, Any]


async def sse_stream(events: AsyncIterator[StreamEvent]) -> StreamingResponse:
    """Create an SSE StreamingResponse from an async iterator of events.

    Args:
        events: Async iterator yielding StreamEvent instances.

    Returns:
        A StreamingResponse with text/event-stream content type.
    """

    async def generate() -> AsyncIterator[str]:
        async for event in events:
            payload = {"event": event.event, **event.data}
            yield f"data: {json.dumps(payload)}\n\n"
        yield 'data: {"event": "done"}\n\n'

    return StreamingResponse(generate(), media_type="text/event-stream")
