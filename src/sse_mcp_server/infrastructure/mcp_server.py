"""MCP Server configuration with tools, resources, and prompts.

This module sets up the MCP server instance and registers all available
tools, resources, and prompts using the tool factory pattern.
"""

import logging
from typing import Any

from mcp import types
from mcp.server import Server
from pydantic import AnyUrl

from sse_mcp_server.infrastructure.tool_factory import (
    CalculatorTool,
    create_simple_tool,
    tool_registry,
)

# Initialize logger
logger = logging.getLogger(__name__)

# Create the MCP Server instance
mcp_server = Server("sse-mcp-server")


def register_tools() -> None:
    """Register all MCP tools."""
    # Register calculator tools using factory
    for operation in ["sum", "subtract", "multiply", "divide"]:
        tool_registry.register(CalculatorTool(operation))

    # Register custom simple tool example
    def get_server_info(_args: dict[str, Any]) -> dict[str, str]:
        """Get server information."""
        return {
            "server": "SSE MCP Server",
            "version": "0.1.0",
            "status": "running",
        }

    info_tool = create_simple_tool(
        name="get_server_info",
        description="Get information about the MCP server",
        properties={},
        required=[],
        handler=get_server_info,
    )
    tool_registry.register(info_tool)


# Register tools on module import
register_tools()


@mcp_server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available resources."""
    return [
        types.Resource(
            uri=AnyUrl("config://app"),
            name="App Config",
            mimeType="text/plain",
        )
    ]


@mcp_server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """Read a specific resource."""
    if str(uri) == "config://app":
        from sse_mcp_server.config.settings import settings

        return f"""Application Configuration:
- Name: {settings.app_name}
- Version: {settings.version}
- Environment: {settings.environment.value}
- Debug: {settings.debug}
- Host: {settings.host}
- Port: {settings.port}
"""
    raise ValueError(f"Resource not found: {uri}")


@mcp_server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools using the tool registry."""
    return tool_registry.list_tools()


@mcp_server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution using the tool registry."""
    try:
        return await tool_registry.execute_tool(name, arguments)
    except (ValueError, KeyError, RuntimeError) as e:
        logger.error("Error executing tool %s: %s", name, e)
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


@mcp_server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """List available prompts."""
    return [
        types.Prompt(
            name="greeting",
            description="Generate a greeting",
            arguments=[
                types.PromptArgument(
                    name="name",
                    description="Name of the person to greet",
                    required=True,
                )
            ],
        )
    ]


@mcp_server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """Generate a prompt."""
    if name == "greeting":
        user_name = (arguments or {}).get("name", "User")
        return types.GetPromptResult(
            description="A friendly greeting",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Hello, {user_name}! How can I help you today?",
                    ),
                )
            ],
        )
    raise ValueError(f"Unknown prompt: {name}")
