"""Agno SDK adapter implementation for LLM interactions."""

from typing import Any, AsyncIterator

from agno.agent import Agent as AgnoAgent
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat

from app.core.config import Settings


class AgnoAdapter:
    """Adapter that uses the Agno SDK for LLM interactions.

    Supports Anthropic (Claude), OpenAI, and Google (Gemini) models
    via the unified Agno interface.
    """

    def __init__(self, settings: Settings) -> None:
        """Initialize with application settings for model configuration."""
        self.settings = settings

    def _get_model(self) -> Claude | OpenAIChat | Gemini:
        """Get the LLM model instance based on configured provider."""
        provider = self.settings.llm_provider
        if provider == "anthropic":
            return Claude(
                id=self.settings.llm_model,
                api_key=self.settings.anthropic_api_key,
            )
        elif provider == "openai":
            return OpenAIChat(
                id=self.settings.llm_model,
                api_key=self.settings.openai_api_key,
            )
        elif provider == "google":
            return Gemini(
                id=self.settings.llm_model,
                api_key=self.settings.google_api_key,
            )
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

    async def invoke(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Send messages to the LLM and get a complete response.

        Creates an Agno Agent with the configured model, runs it with
        the last user message, and returns the response content.
        """
        model = self._get_model()
        agent = AgnoAgent(model=model, markdown=True)

        # Extract the last user message for the agent run
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        response = await agent.arun(user_message)
        content = response.content if response and response.content else ""

        return {"content": content}

    async def stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Stream responses from the LLM as chunks.

        Uses Agno's async streaming to yield response deltas.
        """
        model = self._get_model()
        agent = AgnoAgent(model=model, markdown=True)

        # Extract the last user message
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        response_stream = await agent.arun(user_message, stream=True)
        async for chunk in response_stream:
            if chunk and chunk.content:
                yield {"content": chunk.content}
