"""Main router configuration for the API.

This module aggregates all API routes and provides the main router
for the application.
"""

import logging

from fastapi import APIRouter

from sse_mcp_server.presentation.v1 import api as v1_api

logger = logging.getLogger(__name__)

router = APIRouter()

# Include v1 API routes
router.include_router(v1_api.router, tags=["v1"])
