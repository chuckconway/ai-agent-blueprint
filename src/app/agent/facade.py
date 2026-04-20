"""Main Agent facade that orchestrates tools, interceptors, and LLM adapter."""

from typing import AsyncIterator

from app.agent.adapters.loader import load_adapter
from app.agent.interceptors import AgentRequest, AgentResponse, InterceptorPipeline
from app.agent.streaming import StreamEvent
from app.agent.tools import ToolRegistry, registry
from app.api.middleware.auth import UserContext
from app.core.config import Settings


class Agent:
    """Main agent facade. Orchestrates tools, interceptors, and LLM adapter.

    This is the primary entry point for running agent interactions. It wires
    together the tool registry, interceptor pipeline, and LLM adapter into
    a cohesive execution flow.
    """

    def __init__(self, settings: Settings) -> None:
        """Initialize the agent with application settings.

        Args:
            settings: Application configuration including LLM provider details.
        """
        self.settings = settings
        self.tool_registry: ToolRegistry = registry
        self.interceptors = InterceptorPipeline()
        self._adapter = load_adapter(self._resolve_framework(), settings)

    def _resolve_framework(self) -> str:
        """Map provider to adapter framework. Currently always 'agno'."""
        return "agno"

    async def run(
        self,
        message: str,
        user_context: UserContext | None = None,
        conversation_id: str | None = None,
    ) -> AgentResponse:
        """Run the agent with a user message and return the complete response.

        Args:
            message: The user's input message.
            user_context: Authenticated user information.
            conversation_id: Optional conversation thread identifier.

        Returns:
            The agent's response after interceptor processing.
        """
        request = AgentRequest(
            message=message,
            conversation_id=conversation_id,
            user_id=user_context.user_id if user_context else None,
        )
        request = await self.interceptors.process_request(request)

        messages = [{"role": "user", "content": request.message}]
        tools = (
            self.tool_registry.to_schema() if self.tool_registry.list_tools() else None
        )

        result = await self._adapter.invoke(messages, tools)
        response = AgentResponse(message=result.get("content", ""))
        response = await self.interceptors.process_response(response)
        return response

    async def stream(
        self,
        message: str,
        user_context: UserContext | None = None,
        conversation_id: str | None = None,
    ) -> AsyncIterator[StreamEvent]:
        """Stream agent response as server-sent events.

        Args:
            message: The user's input message.
            user_context: Authenticated user information.
            conversation_id: Optional conversation thread identifier.

        Yields:
            StreamEvent instances with text deltas and completion signals.
        """
        request = AgentRequest(
            message=message,
            conversation_id=conversation_id,
            user_id=user_context.user_id if user_context else None,
        )
        request = await self.interceptors.process_request(request)

        messages = [{"role": "user", "content": request.message}]
        tools = (
            self.tool_registry.to_schema() if self.tool_registry.list_tools() else None
        )

        async for chunk in self._adapter.stream(messages, tools):
            yield StreamEvent(
                event="text_delta", data={"content": chunk.get("content", "")}
            )
