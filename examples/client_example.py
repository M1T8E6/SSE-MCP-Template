"""
Example script showing how to use the MCP server with an MCP client.

This demonstrates connecting to the SSE server and calling tools.
"""

import asyncio
import os

from mcp import types
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client


async def main() -> None:
    """Main function to demonstrate MCP client usage."""
    server_url = f"http://localhost:{os.getenv('APP_PORT', '5001')}{os.getenv('API_V1_STR', '/mcp/v1')}/sse"

    print(f"Connecting to MCP server at {server_url}...")

    async with sse_client(server_url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            print("✓ Connected and initialized")

            # List available tools
            tools_result = await session.list_tools()
            print(f"\nAvailable tools: {len(tools_result.tools)}")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # List available resources
            resources_result = await session.list_resources()
            print(f"\nAvailable resources: {len(resources_result.resources)}")
            for resource in resources_result.resources:
                print(f"  - {resource.name} ({resource.uri})")

            # List available prompts
            prompts_result = await session.list_prompts()
            print(f"\nAvailable prompts: {len(prompts_result.prompts)}")
            for prompt in prompts_result.prompts:
                print(f"  - {prompt.name}: {prompt.description}")

            # Call a tool
            print("\n--- Calling calculate_sum tool ---")
            tool_result = await session.call_tool(
                "calculate_sum", arguments={"a": 5, "b": 3}
            )
            for content in tool_result.content:
                if isinstance(content, types.TextContent):
                    print(f"Result: {content.text}")

            # Read a resource
            print("\n--- Reading resource ---")
            from pydantic import AnyUrl

            resource_uri = AnyUrl("config://app")
            resource_contents = await session.read_resource(resource_uri)
            for content in resource_contents.contents:
                if isinstance(content, types.TextResourceContents):
                    print(f"Resource content: {content.text}")

            # Get a prompt
            print("\n--- Getting prompt ---")
            prompt_result = await session.get_prompt(
                "greeting", arguments={"name": "World"}
            )
            print(f"Prompt description: {prompt_result.description}")
            for message in prompt_result.messages:
                if isinstance(message.content, types.TextContent):
                    print(f"Message: {message.content.text}")


if __name__ == "__main__":
    asyncio.run(main())
