"""
Module for loading configuration for the Secret Hub CLI.
Supports loading from environment variables or a .env file.
"""

from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SecretHubConfig(BaseSettings):
    """Pydantic-based configuration model for SecretHub CLI."""

    model_config = {
        "env_file": ".env",
    }

    GITHUB_TOKEN: str = Field(...)  # Required field from environment


def load_config() -> SecretHubConfig:
    """
    Load the configuration from environment variables or a .env file.

    Returns:
        SecretHubConfig: An instance of the Pydantic configuration model.
    """
    return SecretHubConfig()  # type: ignore[call-arg]
