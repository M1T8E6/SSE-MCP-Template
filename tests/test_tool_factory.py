"""Tests for MCP tool factory."""

# pylint: disable=import-error

import pytest
from mcp import types

from sse_mcp_server.infrastructure.tool_factory import (
    CalculatorTool,
    MCPToolRegistry,
    create_simple_tool,
)


@pytest.mark.asyncio
async def test_calculator_tool_sum() -> None:
    """Test calculator sum tool."""
    tool = CalculatorTool("sum")
    assert tool.name == "calculate_sum"

    result = await tool.execute({"a": 5, "b": 3})
    assert len(result) == 1
    assert isinstance(result[0], types.TextContent)
    assert result[0].text == "8"


@pytest.mark.asyncio
async def test_calculator_tool_multiply() -> None:
    """Test calculator multiply tool."""
    tool = CalculatorTool("multiply")
    assert tool.name == "calculate_multiply"

    result = await tool.execute({"a": 4, "b": 5})
    assert len(result) == 1
    assert isinstance(result[0], types.TextContent)
    assert result[0].text == "20"


@pytest.mark.asyncio
async def test_calculator_tool_divide() -> None:
    """Test calculator divide tool."""
    tool = CalculatorTool("divide")

    result = await tool.execute({"a": 10, "b": 2})
    assert len(result) == 1
    assert isinstance(result[0], types.TextContent)
    assert result[0].text == "5.0"


@pytest.mark.asyncio
async def test_calculator_tool_divide_by_zero() -> None:
    """Test calculator divide by zero."""
    tool = CalculatorTool("divide")

    result = await tool.execute({"a": 10, "b": 0})
    assert len(result) == 1
    assert isinstance(result[0], types.TextContent)
    assert "Error" in result[0].text


@pytest.mark.asyncio
async def test_simple_tool_creation() -> None:
    """Test creating a simple tool."""

    def handler(args: dict) -> str:  # type: ignore[type-arg]
        return f"Hello, {args.get('name', 'World')}!"

    tool = create_simple_tool(
        name="greet",
        description="Greet someone",
        properties={"name": {"type": "string"}},
        required=[],
        handler=handler,
    )

    assert tool.name == "greet"
    result = await tool.execute({"name": "Alice"})
    assert len(result) == 1
    assert isinstance(result[0], types.TextContent)
    assert "Alice" in result[0].text


@pytest.mark.asyncio
async def test_tool_registry() -> None:
    """Test tool registry."""
    registry = MCPToolRegistry()

    # Register tools
    registry.register(CalculatorTool("sum"))
    registry.register(CalculatorTool("multiply"))

    # List tools
    tools = registry.list_tools()
    assert len(tools) == 2
    assert any(t.name == "calculate_sum" for t in tools)
    assert any(t.name == "calculate_multiply" for t in tools)

    # Get tool
    tool = registry.get("calculate_sum")
    assert tool is not None
    assert tool.name == "calculate_sum"

    # Execute tool
    result = await registry.execute_tool("calculate_sum", {"a": 3, "b": 7})
    assert len(result) == 1
    assert isinstance(result[0], types.TextContent)
    assert result[0].text == "10"


@pytest.mark.asyncio
async def test_tool_registry_unknown_tool() -> None:
    """Test executing unknown tool raises error."""
    registry = MCPToolRegistry()

    with pytest.raises(ValueError, match="Unknown tool"):
        await registry.execute_tool("nonexistent", {})
