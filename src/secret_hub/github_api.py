"""
Module for interacting with GitHub API for secrets management.
Provides functions to list, add, and delete secrets in GitHub repositories.
"""

import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

GITHUB_API_URL = "https://api.github.com"
API_VERSION = "2022-11-28"


def list_secrets(repo: str, token: str) -> list:
    """List all secrets in the given repository.

    Args:
        repo (str): The GitHub repository name in the format 'owner/repo'.
        token (str): The GitHub personal access token for authentication.

    Returns:
        list: A list of secret names in the repository.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{repo}/actions/secrets"
    headers = {
        "Authorization": f"token {token}",
        "Accept": f"application/vnd.github+json; api-version={API_VERSION}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return [secret["name"] for secret in response.json().get("secrets", [])]


def get_public_key(repo: str, token: str) -> tuple[str, str]:
    """Retrieve the public key used to encrypt secrets.

    Args:
        repo (str): The GitHub repository name in the format 'owner/repo'.
        token (str): The GitHub personal access token for authentication.

    Returns:
        tuple: The Base64-encoded public key and key_id as a tuple.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{repo}/actions/secrets/public-key"
    headers = {
        "Authorization": f"token {token}",
        "Accept": f"application/vnd.github+json; api-version={API_VERSION}",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    public_key_data = response.json()

    # Use logging instead of print
    logging.info(f"Public Key: {public_key_data['key']}")
    logging.info(f"Key ID: {public_key_data['key_id']}")

    return public_key_data["key"], public_key_data["key_id"]


def create_secret(
    repo: str, name: str, encrypted_value: str, key_id: str, token: str
) -> None:
    """Create or update a secret in the repository.

    Args:
        repo (str): The GitHub repository name in the format 'owner/repo'.
        name (str): The name of the secret.
        encrypted_value (str): The Base64-encoded encrypted secret.
        key_id (str): The key_id of the public key used for encryption.
        token (str): The GitHub personal access token for authentication.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{repo}/actions/secrets/{name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": f"application/vnd.github+json; api-version={API_VERSION}",
    }
    data = {"encrypted_value": encrypted_value, "key_id": key_id}
    response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()


def delete_secret(repo: str, name: str, token: str) -> None:
    """Delete a secret from the repository.

    Args:
        repo (str): The GitHub repository name in the format 'owner/repo'.
        name (str): The name of the secret to delete.
        token (str): The GitHub personal access token for authentication.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    url = f"{GITHUB_API_URL}/repos/{repo}/actions/secrets/{name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": f"application/vnd.github+json; api-version={API_VERSION}",
    }
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
