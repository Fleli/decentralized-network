
import secrets

from ... import config


def generate_root_key(num_bytes: int | None = None) -> bytes:
    """Generate cryptographically secure root-key material.

    A root key is the master secret from which child keys are derived, so
    32 random bytes is a sensible default. Use a larger size only when a
    concrete downstream construction requires it.
    """

    if num_bytes is None:
        num_bytes = config.DEFAULT_ROOT_KEY_BYTES

    if num_bytes <= 0:
        raise ValueError("Root key length must be a positive number of bytes.")

    return secrets.token_bytes(num_bytes)
