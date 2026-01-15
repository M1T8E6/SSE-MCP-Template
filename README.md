# SSE MCP Server Template

A production-ready, Domain-Driven Design (DDD) inspired template for building Model Context Protocol (MCP) servers using Python, FastAPI, and Server-Sent Events (SSE).

## Features

- **Production Ready**: Structured for scalability and maintainability
- **SSE Transport**: Native support for Server-Sent Events transport for MCP
- **FastAPI**: Built on top of high-performance FastAPI
- **Type Safety**: Strict type checking with `mypy` and comprehensive type hints
- **DDD Architecture**: Clean separation of Domain, Application, Infrastructure, and Presentation layers
- **Testing**: Configured with `pytest` and `pytest-asyncio`

## Project Structure

```
src/sse_mcp_server/
├── domain/           # Entities, Value Objects, Protocols
│   ├── models.py     # Domain models and exceptions
│   └── protocols.py  # Domain interfaces
├── application/      # Application Services, Use Cases
│   └── services.py   # Business logic implementation
├── infrastructure/   # External implementations (MCP Server, adapters)
│   └── mcp_server.py # MCP server configuration
├── presentation/     # API Endpoints (SSE, HTTP)
│   └── api.py        # FastAPI routes and SSE handlers
└── main.py           # Application entry point
```

## Prerequisites

- Python 3.10+
- `pip` or `uv`

## Getting Started

### 1. Installation

```bash
# Clone the template
git clone git@github.com:M1T8E6/SSE-MCP-Template.git
cd sse-mcp-server 

# Open the project in the dev-container or set up a virtual environment
uv venv venv
source venv/bin/activate
```

### 2. Configuration

```bash
make prepare-env
```

### 3. Running the Server

```bash
make run
```

**Available endpoints:**
- Health Check: `http://0.0.0.0:5001/mcp/v1/health`
- SSE Connection: `http://0.0.0.0:5001/mcp/v1/sse`
- MCP Messages: `http://0.0.0.0:5001/mcp/v1/messages` (POST)

### 4. Development Workflow

```bash
# Run tests
make test

# Lint and type check
make lint

# Clean cache and build files
make clean
```

## Architecture Details

### Domain Layer
Contains pure business logic and interfaces (Protocols). It has no dependencies on outer layers.
- **models.py**: Domain entities, value objects, and exceptions
- **protocols.py**: Domain service interfaces

### Application Layer
Implements use cases and application services using domain protocols.
- **services.py**: Application service implementations

### Infrastructure Layer
Implements protocols defined in the Domain and provides external integrations.
- **mcp_server.py**: MCP Server configuration with tools, resources, and prompts

### Presentation Layer
Handles HTTP requests and SSE connections. Bridges the web world to application services.
- **api.py**: FastAPI routes and SSE transport handling

## MCP Integration

This template uses the low-level `mcp.server.Server` to allow full integration with FastAPI.

- The `SseServerTransport` is properly integrated with FastAPI routes
- Tools and Resources are defined in `infrastructure/mcp_server.py`
- The SSE endpoint establishes the connection and manages the MCP server lifecycle
- Messages are POSTed to a separate endpoint for processing

### Example: Adding a New Tool

Edit `src/sse_mcp_server/infrastructure/mcp_server.py`:

```python
@mcp_server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="your_tool",
            description="Description of your tool",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string"},
                },
                "required": ["param"],
            },
        )
    ]

@mcp_server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, object] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "your_tool":
        param = arguments.get("param") if arguments else None
        result = f"Tool executed with: {param}"
        return [types.TextContent(type="text", text=result)]
    raise ValueError(f"Unknown tool: {name}")
```

## Testing

Run tests with:

```bash
make test
```

## License

MIT
