
# Secret Hub Python CLI

A Python-based Command Line Interface (CLI) for managing GitHub repository secrets. The `Secret Hub` CLI allows you to list, add, and delete secrets from GitHub repositories, using encrypted communication with the GitHub API.

> **Note**: This project is loosely based on [DannyBen's secret_hub](https://github.com/DannyBen/secret_hub). We may have even stolen the name! ;)

## Features

- **List secrets**: Retrieve and display the list of all secrets in a given GitHub repository.
- **Add secrets**: Add secrets to a GitHub repository from a JSON file, with encryption using LibSodium.
- **Delete secrets**: Remove secrets from a GitHub repository.

## Table of Contents

- [Secret Hub Python CLI](#secret-hub-python-cli)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Available Commands:](#available-commands)
  - [Examples](#examples)
    - [1. **List Secrets in a Repository**](#1-list-secrets-in-a-repository)
    - [2. **Bulk Add Secrets from a JSON File**](#2-bulk-add-secrets-from-a-json-file)
    - [3. **Delete a Secret**](#3-delete-a-secret)
  - [Dependencies](#dependencies)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Requirements

This project requires **PDM** (Python Dependency Manager) to handle Python dependencies.

To install PDM, follow the [official installation instructions](https://pdm.fming.dev/latest/#installation):

```bash
pip install pdm
```

Make sure you have Python 3.10 installed, as this project requires Python 3.10 or higher.

## Installation

Once PDM is installed, you can install the Secret Hub CLI's dependencies by following these steps:

1. **Clone the repository**:

    ```bash
    git clone git@github.com:yourusername/secret_hub_python.git
    cd secret_hub_python
    ```

2. **Install dependencies using PDM**:

    ```bash
    pdm install
    ```

3. **Activate the virtual environment**:

    ```bash
    pdm venv activate
    ```

## Configuration

The CLI loads the GitHub token from environment variables, a `.env` file, or via the `--token` option in each command.

1. **Environment Variables**: You can set the `GITHUB_TOKEN` environment variable directly.

    ```bash
    export GITHUB_TOKEN=your_github_token_here
    ```

2. **.env File**: If you prefer, you can store your GitHub token in a `.env` file in the project root directory. Pydantic will automatically load this file if environment variables are not set.

    Here's an example `.env` file:

    ```env
    # .env file

    GITHUB_TOKEN=your_github_token_here
    ```

3. **Command Line Option**: The GitHub token can also be passed directly via the `--token` option in each command.

    For example:

    ```bash
    python cli.py list-secrets owner/repo --token your_github_token_here
    ```

Pydantic automatically loads and validates the token from either the environment, the `.env` file, or the `--token` option, ensuring your configuration is easy to manage and secure.

## Usage

To use the CLI, simply run the `cli.py` script with the desired command.

### Available Commands:

- `list-secrets`: Lists all the secrets in a GitHub repository.
- `bulk-add-secrets`: Adds secrets to a GitHub repository from a JSON file.
- `delete-secret`: Deletes a secret from a GitHub repository.

## Examples

### 1. **List Secrets in a Repository**

To list all secrets in a repository:

```bash
python cli.py list-secrets owner/repo --token YOUR_TOKEN
```

### 2. **Bulk Add Secrets from a JSON File**

To add secrets to a repository from a JSON file:

```bash
python cli.py bulk-add-secrets owner/repo secrets.json --token YOUR_TOKEN
```

The JSON file (`secrets.json`) should contain key-value pairs of secret names and values:

```json
{
    "SECRET_NAME_1": "secret_value_1",
    "SECRET_NAME_2": "secret_value_2"
}
```

### 3. **Delete a Secret**

To delete a specific secret from a repository:

```bash
python cli.py delete-secret owner/repo SECRET_NAME --token YOUR_TOKEN
```

## Dependencies

The project requires the following dependencies, managed via **PDM**:

- `requests`: HTTP library for sending requests to the GitHub API.
- `pynacl`: Python bindings for the LibSodium encryption library.
- `click`: Python package for building command-line interfaces.
- `cfs-config-library`: Custom configuration library for dynamic settings management.
- `cryptography`: Provides cryptographic recipes and primitives to Python developers.

These are defined in the `pyproject.toml` file.

## Contributing

If you would like to contribute to this project:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please ensure all new code follows the project's coding standards and includes relevant tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by [DannyBen's secret_hub](https://github.com/DannyBen/secret_hub). Thanks for the great work!