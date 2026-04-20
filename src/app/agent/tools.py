"""Tool decorator and registry for the agent layer."""

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ToolDefinition:
    """Metadata for a registered tool."""

    name: str
    description: str
    func: Callable[..., Any]
    requires_approval: bool = False
    parameters: dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    """Registry of available tools for the agent.

    Tools are registered via the decorator pattern and can be exported
    as OpenAI-style function schemas for LLM consumption.
    """

    def __init__(self) -> None:
        """Initialize an empty tool registry."""
        self._tools: dict[str, ToolDefinition] = {}

    def register(
        self,
        name: str,
        description: str,
        requires_approval: bool = False,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator to register a function as an agent tool.

        Args:
            name: Unique tool name.
            description: Human-readable description for the LLM.
            requires_approval: Whether tool execution needs user approval.
        """

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            params = self._extract_parameters(func)
            self._tools[name] = ToolDefinition(
                name=name,
                description=description,
                func=func,
                requires_approval=requires_approval,
                parameters=params,
            )
            return func

        return decorator

    def get(self, name: str) -> ToolDefinition | None:
        """Look up a tool by name, returning None if not found."""
        return self._tools.get(name)

    def list_tools(self) -> list[ToolDefinition]:
        """Return all registered tools."""
        return list(self._tools.values())

    def to_schema(self) -> list[dict[str, Any]]:
        """Convert tools to OpenAI-style function schema for LLM."""
        schemas: list[dict[str, Any]] = []
        for tool_def in self._tools.values():
            schemas.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool_def.name,
                        "description": tool_def.description,
                        "parameters": {
                            "type": "object",
                            "properties": tool_def.parameters,
                            "required": [
                                k
                                for k, v in tool_def.parameters.items()
                                if not v.get("optional", False)
                            ],
                        },
                    },
                }
            )
        return schemas

    def _extract_parameters(self, func: Callable[..., Any]) -> dict[str, Any]:
        """Extract parameter schema from function signature type hints."""
        sig = inspect.signature(func)
        params: dict[str, Any] = {}
        type_map = {str: "string", int: "integer", float: "number", bool: "boolean"}

        for param_name, param in sig.parameters.items():
            if param_name in ("self", "cls"):
                continue
            annotation = param.annotation
            json_type = type_map.get(annotation, "string")
            params[param_name] = {"type": json_type}
            if param.default is not inspect.Parameter.empty:
                params[param_name]["optional"] = True

        return params


# Global registry
registry = ToolRegistry()
tool = registry.register  # Convenience alias: @tool("name", "description")
