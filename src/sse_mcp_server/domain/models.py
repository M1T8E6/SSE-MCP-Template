from typing import NewType

from pydantic import BaseModel, Field

# Using NewType for semantic aliases
MessageId = NewType("MessageId", str)
SessionId = NewType("SessionId", str)


class DomainError(Exception):
    """Base exception for domain errors."""


class ResourceNotFound(DomainError):
    """Raised when a requested resource is not found."""


class HealthCheckRequest(BaseModel):
    """Model representing a health check request."""

    check_type: str = Field(..., description="The type of health check requested.")


class HealthCheckResponse(BaseModel):
    """Model representing a health check response."""

    status: str = Field(..., description="The status of the service.")
    version: str = Field(..., description="The version of the service.")
