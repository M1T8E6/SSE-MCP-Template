"""Application configuration management.

This module handles environment-specific configuration loading for the ADK template.
"""

import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv


class Environment(str, Enum):
    """Application environment types."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TEST = "test"


def get_environment() -> Environment:
    """Get the current environment.

    Returns:
        Environment: The current environment
    """
    match os.getenv("APP_ENV", "development").lower():
        case "production" | "prod":
            return Environment.PRODUCTION
        case "staging" | "stage":
            return Environment.STAGING
        case "test":
            return Environment.TEST
        case _:
            return Environment.DEVELOPMENT


def load_env_file() -> str | None:
    """Load environment-specific .env file."""
    env = get_environment()
    base_dir = Path(__file__).parent.parent.parent.parent

    env_files = [
        base_dir / f".env.{env.value}.local",
        base_dir / f".env.{env.value}",
        base_dir / ".env.local",
        base_dir / ".env",
    ]

    for env_file in env_files:
        if env_file.is_file():
            load_dotenv(dotenv_path=env_file)
            return str(env_file)

    return None


def parse_list_from_env(env_key: str, default: list | None = None) -> list:
    """Parse a comma-separated list from an environment variable."""
    value = os.getenv(env_key)
    if not value:
        return default or []

    value = value.strip("\"'")
    if "," not in value:
        return [value]
    return [item.strip() for item in value.split(",") if item.strip()]


# Load env file on module import
ENV_FILE = load_env_file()


@dataclass
class CorsConfig:
    """CORS configuration."""

    allowed_origins: list = field(
        default_factory=lambda: parse_list_from_env("ALLOWED_ORIGINS", ["*"])
    )


@dataclass
class LogConfig:
    """Logging configuration."""

    log_dir: Path = field(default_factory=lambda: Path(os.getenv("LOG_DIR", "logs")))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_format: str = field(default_factory=lambda: os.getenv("LOG_FORMAT", "json"))


@dataclass
class RateLimitConfig:
    """Rate limiting configuration."""

    default: list = field(
        default_factory=lambda: parse_list_from_env(
            "RATE_LIMIT_DEFAULT", ["200 per day", "50 per hour"]
        )
    )
    endpoints: dict = field(
        default_factory=lambda: {
            "agents": parse_list_from_env("RATE_LIMIT_AGENTS", ["60 per minute"]),
            "health": parse_list_from_env("RATE_LIMIT_HEALTH", ["20 per minute"]),
        }
    )


@dataclass
class RedisConfig:
    """Redis configuration."""

    url: str | None = field(default_factory=lambda: os.getenv("REDIS_URL") or None)
    ttl: int = field(
        default_factory=lambda: int(os.getenv("REDIS_TTL", "86400"))
    )  # Default 24 hours


class Settings:
    """Application settings for ADK template.

    This class loads configuration from environment variables and provides
    access to application settings with proper naming conventions.
    """

    def __init__(self):
        """Initialize application settings from environment variables."""
        # Environment
        self.environment = get_environment()

        # Database
        self.database_path = os.getenv("DATABASE_PATH", "data/agent_hub.db")

        # Application Settings
        self.app_name = os.getenv("APP_NAME", "Agent Hub")
        self.version = os.getenv("VERSION", "1.0.0")
        self.description = os.getenv(
            "DESCRIPTION",
            "A modular template for AI agents using Google ADK with hexagonal architecture",
        )
        self.api_v1_str = os.getenv("API_V1_STR", "/mcp/v1")
        self.host = os.getenv("APP_HOST", "0.0.0.0")
        self.port = int(os.getenv("APP_PORT", "5001"))
        self.debug = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

        # Configuration objects
        self.cors = CorsConfig()
        self.logging = LogConfig()
        self.rate_limit = RateLimitConfig()
        self.redis = RedisConfig()

        # Apply environment-specific settings
        self._apply_environment_settings()

    # Compatibility properties for direct access
    @property
    def allowed_origins(self) -> list:
        """Get allowed origins for CORS."""
        return self.cors.allowed_origins

    @property
    def log_dir(self) -> Path:
        """Get log directory."""
        return self.logging.log_dir

    @property
    def log_level(self) -> str:
        """Get log level."""
        return self.logging.log_level

    @property
    def log_format(self) -> str:
        """Get log format."""
        return self.logging.log_format

    @property
    def rate_limit_default(self) -> list:
        """Get default rate limit."""
        return self.rate_limit.default

    @property
    def rate_limit_endpoints(self) -> dict:
        """Get rate limit endpoints."""
        return self.rate_limit.endpoints

    def _apply_environment_settings(self):
        """Apply environment-specific settings."""
        env_settings = {
            Environment.DEVELOPMENT: {
                "debug": True,
                "log_level": "DEBUG",
                "log_format": "console",
            },
            Environment.STAGING: {
                "debug": False,
                "log_level": "INFO",
            },
            Environment.PRODUCTION: {
                "debug": False,
                "log_level": "WARNING",
            },
            Environment.TEST: {
                "debug": True,
                "log_level": "DEBUG",
                "log_format": "console",
            },
        }

        current_env_settings = env_settings.get(self.environment, {})
        for key, value in current_env_settings.items():
            if key.upper() not in os.environ:
                if key.startswith("log_"):
                    setattr(self.logging, key, value)
                else:
                    setattr(self, key, value)

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION

    def get_cors_config(self) -> dict:
        """Get CORS configuration as a dictionary."""
        return {
            "allow_origins": self.allowed_origins,
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        }


# Create settings instance
settings = Settings()
