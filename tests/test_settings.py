"""Tests for settings configuration."""

# pylint: disable=import-error

from sse_mcp_server.config.settings import Environment, settings


def test_settings_loaded() -> None:
    """Test that settings are loaded."""
    assert settings is not None
    assert settings.app_name is not None
    assert settings.version is not None


def test_settings_environment() -> None:
    """Test environment detection."""
    assert isinstance(settings.environment, Environment)


def test_settings_cors_config() -> None:
    """Test CORS configuration."""
    cors_config = settings.get_cors_config()
    assert "allow_origins" in cors_config
    assert "allow_credentials" in cors_config
    assert cors_config["allow_credentials"] is True


def test_settings_host_and_port() -> None:
    """Test host and port settings."""
    assert settings.host is not None
    assert isinstance(settings.port, int)
    assert settings.port > 0


def test_settings_api_prefix() -> None:
    """Test API prefix."""
    assert settings.api_v1_str == "/api/v1"


def test_environment_helpers() -> None:
    """Test environment helper methods."""
    # These methods should work without errors
    is_dev = settings.is_development()
    is_prod = settings.is_production()

    assert isinstance(is_dev, bool)
    assert isinstance(is_prod, bool)

    # Can't be both dev and prod
    if is_dev:
        assert not is_prod
    if is_prod:
        assert not is_dev
