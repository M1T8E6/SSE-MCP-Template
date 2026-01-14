# SSE MCP Server Template

A production-ready, Domain-Driven Design (DDD) inspired template for building Model Context Protocol (MCP) servers using Python, FastAPI, and Server-Sent Events (SSE).

## Features

- **Production Ready**: Structured for scalability and maintainability
- **SSE Transport**: Native support for Server-Sent Events transport for MCP
- **FastAPI**: Built on top of high-performance FastAPI
- **Type Safety**: Strict type checking with `mypy` and comprehensive type hints
- **DDD Architecture**: Clean separation of Domain, Application, Infrastructure, and Presentation layers
- **Testing**: Configured with `pytest` and `pytest-asyncio`
- **Modern Tooling**: `pyproject.toml` setup, `ruff` for linting/formatting, `Makefile` for common tasks

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
git clone <your-repo-url>
cd sse-mcp-server

# Create virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
make install
# or
pip install -e ".[dev]"
```

### 2. Configuration

Create a `.env` file in the root directory (optional):

```ini
PROJECT_NAME="My MCP Server"
DEBUG=true
VERSION="0.1.0"
```

### 3. Running the Server

Start the development server with hot-reload:

```bash
make dev
```

The server will start at `http://0.0.0.0:5035`.

**Available endpoints:**
- Health Check: `http://0.0.0.0:5035/api/v1/health`
- SSE Connection: `http://0.0.0.0:5035/api/v1/sse`
- MCP Messages: `http://0.0.0.0:5035/api/v1/messages` (POST)

### 4. Development Workflow

```bash
# Run tests
make test

# Run tests with coverage
make test-coverage

# Lint and type check
make lint

# Format code
make format

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
pytest
# or
make test
```

Run tests with coverage:

```bash
make test-coverage
```

## Deployment

For production deployment:

1. Set `DEBUG=false` in your `.env` file
2. Use a production-grade ASGI server:
   ```bash
   uvicorn sse_mcp_server.main:app --host 0.0.0.0 --port 5035 --workers 4
   ```
3. Consider using a reverse proxy (nginx, traefik) in front of uvicorn
4. Enable HTTPS/TLS for secure connections

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT
