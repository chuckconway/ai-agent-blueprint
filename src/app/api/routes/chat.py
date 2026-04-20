"""Chat API routes for agent interactions."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.agent.facade import Agent
from app.agent.streaming import sse_stream
from app.api.core.schemas import ApiResponse
from app.api.middleware.auth import UserContext, get_current_user
from app.core.config import get_settings

router = APIRouter()


class ChatRequest(BaseModel):
    """Schema for incoming chat requests."""

    message: str
    conversation_id: str | None = None


def get_agent() -> Agent:
    """Create an Agent instance from current settings."""
    return Agent(get_settings())


@router.post("/")
async def chat(
    request: ChatRequest,
    user: UserContext = Depends(get_current_user),
) -> ApiResponse:
    """Send a message and get a complete response.

    Args:
        request: The chat message and optional conversation context.
        user: Authenticated user from JWT token.

    Returns:
        ApiResponse wrapping the agent's message and any tool calls.
    """
    agent = get_agent()
    response = await agent.run(
        request.message,
        user_context=user,
        conversation_id=request.conversation_id,
    )
    return ApiResponse(
        data={"message": response.message, "tool_calls": response.tool_calls}
    )


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    user: UserContext = Depends(get_current_user),
):
    """Stream a response via Server-Sent Events.

    Args:
        request: The chat message and optional conversation context.
        user: Authenticated user from JWT token.

    Returns:
        SSE stream with text_delta events followed by a done event.
    """
    agent = get_agent()
    events = agent.stream(
        request.message,
        user_context=user,
        conversation_id=request.conversation_id,
    )
    return await sse_stream(events)
