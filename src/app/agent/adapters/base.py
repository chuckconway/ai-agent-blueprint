"""Runtime adapter protocol for LLM providers."""

from typing import Any, AsyncIterator, Protocol


class RuntimeAdapter(Protocol):
    """Protocol for LLM provider adapters.

    All adapters must implement invoke (request/response) and stream
    (server-sent event style) methods.
    """

    async def invoke(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Send messages to the LLM and get a complete response.

        Args:
            messages: Conversation history in OpenAI message format.
            tools: Optional tool schemas for function calling.

        Returns:
            Response dict with at minimum a "content" key.
        """
        ...

    async def stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Stream responses from the LLM.

        Args:
            messages: Conversation history in OpenAI message format.
            tools: Optional tool schemas for function calling.

        Yields:
            Response chunks with at minimum a "content" key.
        """
        ...
