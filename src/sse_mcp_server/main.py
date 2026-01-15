from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.routing import Route as StarletteRoute

from sse_mcp_server.config.settings import settings
from sse_mcp_server.presentation.router import router as api_router
from sse_mcp_server.presentation.v1 import sse_transport


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan events for application startup and shutdown."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    lifespan=lifespan,
    redirect_slashes=False,  # Disable automatic trailing slash redirects
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    formatted_errors = [
        {
            "field": " -> ".join([str(p) for p in e["loc"] if p != "body"]),
            "message": e["msg"],
        }
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": formatted_errors},
    )


app.include_router(api_router, prefix=settings.api_v1_str)


# Add the SSE messages POST endpoint as a raw ASGI app using Starlette's routing
# We need to bypass FastAPI's response handling since handle_post_message
# is a raw ASGI app that handles its own response
class ASGIRoute(StarletteRoute):
    """Custom route that treats the endpoint as a raw ASGI app."""

    async def handle(self, scope, receive, send):
        """Handle the request by calling the endpoint as a raw ASGI app."""
        await self.endpoint(scope, receive, send)


app.router.routes.append(
    ASGIRoute(
        path=f"{settings.api_v1_str}/messages",
        endpoint=sse_transport.handle_post_message,
        methods=["POST"],
    )
)

if __name__ == "__main__":
    import uvicorn

    # Allow running via `python -m sse_mcp_server.main`
    # Using the package module path ensures the module is discoverable when
    # running with the -m switch from the project root.
    uvicorn.run(
        "sse_mcp_server.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


def main() -> None:  # pragma: no cover - simple entry helper for module runner
    """Entrypoint used by `python -m sse_mcp_server.main`.

    When run as a module the `__main__` block will execute and start
    uvicorn using the package-qualified path so external `python -m` can
    resolve the module correctly.
    """
    # Delegate to the __main__ behaviour
    import sys

    if sys.argv[0].endswith("__main__.py"):
        # When invoked via `python -m sse_mcp_server.main` this module
        # will run the `__main__` block above; ensure we call it explicitly
        # to keep behavior consistent for other invocation patterns.
        pass
