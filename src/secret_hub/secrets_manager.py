"""
Module for encrypting secrets using NaCl (LibSodium) for GitHub secret management.
"""

import base64
from nacl import public


def encrypt_secret(secret_value: str, public_key: str) -> str:
    """Encrypt the secret using LibSodium.

    Args:
        secret_value (str): The plaintext secret that needs to be encrypted.
        public_key (str): The Base64-encoded public key used to encrypt the secret.

    Returns:
        str: The Base64-encoded encrypted secret.

    Raises:
        ValueError: If the public key cannot be decoded.
    """
    # Input validation
    if not isinstance(secret_value, str):
        raise ValueError("secret_value must be a string.")
    if not isinstance(public_key, str):
        raise ValueError("public_key must be a Base64-encoded string.")

    try:
        # Decode the Base64-encoded public key
        public_key_bytes = base64.b64decode(public_key)
    except Exception as e:
        raise ValueError(f"Failed to decode public key: {e}")

    # Create a PublicKey object from the raw bytes
    public_key_obj = public.PublicKey(public_key_bytes)

    # Encrypt the secret using LibSodium's sealed box
    sealed_box = public.SealedBox(public_key_obj)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))

    # Return the Base64-encoded encrypted secret
    return base64.b64encode(encrypted).decode("utf-8")
