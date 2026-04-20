"""Request/response interceptor pipeline for the agent layer."""

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class AgentRequest:
    """Represents an incoming agent request."""

    message: str
    conversation_id: str | None = None
    user_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResponse:
    """Represents an agent response."""

    message: str
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class RequestInterceptor(Protocol):
    """Intercepts requests before they reach the LLM."""

    async def intercept(self, request: AgentRequest) -> AgentRequest:
        """Transform or enrich the request before LLM processing."""
        ...


class ResponseInterceptor(Protocol):
    """Intercepts responses before they reach the user."""

    async def intercept(self, response: AgentResponse) -> AgentResponse:
        """Transform or enrich the response before returning to the user."""
        ...


class InterceptorPipeline:
    """Manages ordered chains of request and response interceptors.

    Interceptors run in registration order for requests (first-in, first-run)
    and in registration order for responses.
    """

    def __init__(self) -> None:
        """Initialize with empty interceptor chains."""
        self._request_interceptors: list[RequestInterceptor] = []
        self._response_interceptors: list[ResponseInterceptor] = []

    def add_request_interceptor(self, interceptor: RequestInterceptor) -> None:
        """Add a request interceptor to the end of the chain."""
        self._request_interceptors.append(interceptor)

    def add_response_interceptor(self, interceptor: ResponseInterceptor) -> None:
        """Add a response interceptor to the end of the chain."""
        self._response_interceptors.append(interceptor)

    async def process_request(self, request: AgentRequest) -> AgentRequest:
        """Run the request through all registered request interceptors."""
        for interceptor in self._request_interceptors:
            request = await interceptor.intercept(request)
        return request

    async def process_response(self, response: AgentResponse) -> AgentResponse:
        """Run the response through all registered response interceptors."""
        for interceptor in self._response_interceptors:
            response = await interceptor.intercept(response)
        return response
