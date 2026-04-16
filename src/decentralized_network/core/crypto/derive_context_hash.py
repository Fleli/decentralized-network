import hashlib
import hmac


def derive_context_hash(root_key: bytes, context: str) -> bytes:
    if not root_key:
        raise ValueError("Root key must not be empty.")

    if not context:
        raise ValueError("Context must not be empty.")

    context_bytes = context.encode("utf-8")
    return hmac.new(root_key, context_bytes, hashlib.sha256).digest()
