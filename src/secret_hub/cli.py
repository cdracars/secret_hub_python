"""
Command-line interface (CLI) for managing GitHub repository secrets.
Uses Click for handling commands like listing, adding, and deleting secrets.
"""

import click
import json
from secret_hub import github_api, secrets_manager
from secret_hub.config import load_config


# Load configuration dynamically
config = load_config()


@click.group()
def cli() -> None:
    """SecretHub CLI to manage GitHub repository secrets."""
    pass


def get_token(token: str) -> str:
    """
    Get the GitHub token from the CLI argument or from the dynamically loaded config.

    Args:
        token (str): GitHub Personal Access Token provided via CLI option.

    Returns:
        str: GitHub token, either from CLI or from config.
    """
    if token:
        return token
    return config.GITHUB_TOKEN


@cli.command()
@click.argument("repo")
@click.option("--token", help="GitHub Personal Access Token")
def list_secrets(repo: str, token: str) -> None:
    """List secrets in a GitHub repository.

    Args:
        repo (str): The GitHub repository name in the format 'owner/repo'.
        token (str): GitHub Personal Access Token for authentication (optional).
    """
    token = get_token(token)
    if not token:
        click.echo("Error: GitHub token not provided and not found in config")
        return

    secrets = github_api.list_secrets(repo, token)
    click.echo(f"Secrets in {repo}:")
    for secret in secrets:
        click.echo(secret)


@cli.command()
@click.argument("repo")
@click.argument("secrets_file", type=click.Path(exists=True))
@click.option("--token", help="GitHub Personal Access Token")
def bulk_add_secrets(repo: str, secrets_file: str, token: str) -> None:
    """
    Add multiple secrets to a GitHub repository from a JSON file.

    Args:
        repo (str): The GitHub repository name in the format 'owner/repo'.
        secrets_file (str): Path to the JSON file containing secret names and values.
        token (str): GitHub Personal Access Token for authentication (optional).

    The JSON file should contain key-value pairs representing secret names and their values.
    """
    token = get_token(token)
    if not token:
        click.echo("Error: GitHub token not provided and not found in config")
        return

    public_key, key_id = github_api.get_public_key(repo, token)

    # Load secrets from the JSON file
    with open(secrets_file, "r") as file:
        secrets = json.load(file)

    for secret_name, secret_value in secrets.items():
        encrypted_value = secrets_manager.encrypt_secret(secret_value, public_key)
        github_api.create_secret(repo, secret_name, encrypted_value, key_id, token)
        click.echo(f"Secret {secret_name} added to {repo}.")

    click.echo("All secrets have been added.")


@cli.command()
@click.argument("repo")
@click.argument("secret_name")
@click.option("--token", help="GitHub Personal Access Token")
def delete_secret(repo: str, secret_name: str, token: str) -> None:
    """Delete a secret from a GitHub repository.

    Args:
        repo (str): The GitHub repository name in the format 'owner/repo'.
        secret_name (str): The name of the secret to delete.
        token (str): GitHub Personal Access Token for authentication (optional).
    """
    token = get_token(token)
    if not token:
        click.echo("Error: GitHub token not provided and not found in config")
        return

    github_api.delete_secret(repo, secret_name, token)
    click.echo(f"Secret {secret_name} deleted from {repo}.")


if __name__ == "__main__":
    cli()
