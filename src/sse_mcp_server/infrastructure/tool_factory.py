"""MCP Tool Factory for creating tools in a modular and DRY way.

This module provides a factory pattern for creating MCP tools with less boilerplate
and better type safety.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable

from mcp import types


class MCPTool(ABC):
    """Base class for MCP tools."""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
    ):
        """Initialize MCP tool.

        Args:
            name: Tool name
            description: Tool description
            input_schema: JSON schema for input validation
        """
        self.name = name
        self.description = description
        self.input_schema = input_schema

    def to_mcp_tool(self) -> types.Tool:
        """Convert to MCP Tool type.

        Returns:
            types.Tool: MCP tool definition
        """
        return types.Tool(
            name=self.name,
            description=self.description,
            inputSchema=self.input_schema,
        )

    @abstractmethod
    async def execute(
        self, arguments: dict[str, Any]
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Execute the tool with given arguments.

        Args:
            arguments: Tool arguments

        Returns:
            List of content blocks

        Raises:
            ValueError: If arguments are invalid
        """


class SimpleTool(MCPTool):
    """Simple tool that executes a function."""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any],
        handler: Callable[[dict[str, Any]], str | dict[str, Any]],
    ):
        """Initialize simple tool.

        Args:
            name: Tool name
            description: Tool description
            input_schema: JSON schema for input validation
            handler: Async or sync function to execute
        """
        super().__init__(name, description, input_schema)
        self.handler = handler

    async def execute(
        self, arguments: dict[str, Any]
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Execute the tool handler.

        Args:
            arguments: Tool arguments

        Returns:
            List of text content with result
        """
        import inspect

        if inspect.iscoroutinefunction(self.handler):
            result = await self.handler(arguments)
        else:
            result = self.handler(arguments)

        if isinstance(result, dict):
            import json

            result_text = json.dumps(result, indent=2)
        else:
            result_text = str(result)

        return [types.TextContent(type="text", text=result_text)]


class CalculatorTool(MCPTool):
    """Calculator tool for arithmetic operations."""

    def __init__(self, operation: str):
        """Initialize calculator tool.

        Args:
            operation: Operation type (sum, subtract, multiply, divide)
        """
        operations = {
            "sum": ("Calculate the sum of two numbers", "+"),
            "subtract": ("Subtract second number from first", "-"),
            "multiply": ("Multiply two numbers", "*"),
            "divide": ("Divide first number by second", "/"),
        }

        if operation not in operations:
            raise ValueError(f"Unknown operation: {operation}")

        desc, _ = operations[operation]
        super().__init__(
            name=f"calculate_{operation}",
            description=desc,
            input_schema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        )
        self.operation = operation

    async def execute(
        self, arguments: dict[str, Any]
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Execute calculation.

        Args:
            arguments: Tool arguments with 'a' and 'b' numbers

        Returns:
            List with calculation result
        """
        a = arguments.get("a")
        b = arguments.get("b")

        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError("Arguments must be numbers")

        operations = {
            "sum": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else None,
        }

        result = operations[self.operation](a, b)

        if result is None:
            return [types.TextContent(type="text", text="Error: Division by zero")]

        return [types.TextContent(type="text", text=str(result))]


class MCPToolRegistry:
    """Registry for managing MCP tools."""

    def __init__(self):
        """Initialize tool registry."""
        self._tools: dict[str, MCPTool] = {}

    def register(self, tool: MCPTool) -> None:
        """Register a tool.

        Args:
            tool: Tool to register
        """
        self._tools[tool.name] = tool

    def get(self, name: str) -> MCPTool | None:
        """Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(name)

    def list_tools(self) -> list[types.Tool]:
        """List all registered tools as MCP tools.

        Returns:
            List of MCP tool definitions
        """
        return [tool.to_mcp_tool() for tool in self._tools.values()]

    async def execute_tool(
        self, name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Execute a tool by name.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool not found or arguments invalid
        """
        tool = self.get(name)
        if not tool:
            raise ValueError(f"Unknown tool: {name}")

        if arguments is None:
            arguments = {}

        return await tool.execute(arguments)


# Create global registry
tool_registry = MCPToolRegistry()


def create_simple_tool(
    name: str,
    description: str,
    properties: dict[str, Any],
    required: list[str],
    handler: Callable[[dict[str, Any]], str | dict[str, Any]],
) -> SimpleTool:
    """Factory function to create a simple tool.

    Args:
        name: Tool name
        description: Tool description
        properties: Input properties schema
        required: Required property names
        handler: Function to execute

    Returns:
        SimpleTool instance
    """
    input_schema = {
        "type": "object",
        "properties": properties,
        "required": required,
    }

    return SimpleTool(name, description, input_schema, handler)
