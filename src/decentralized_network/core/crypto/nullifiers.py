import hashlib
import hmac


NULLIFIER_DOMAIN_LABEL = "nullifier"


def canonicalize_scope(scope: str) -> bytes:
    if not scope:
        raise ValueError("Scope must not be empty.")

    return scope.encode("utf-8")


def derive_nullifier_domain_secret(root_secret: bytes, domain_label: str) -> bytes:
    if not root_secret:
        raise ValueError("Root secret must not be empty.")

    if not domain_label:
        raise ValueError("Domain label must not be empty.")

    return hmac.new(root_secret, domain_label.encode("utf-8"), hashlib.sha256).digest()


def hash_scope(scope: str) -> bytes:
    return hashlib.sha256(canonicalize_scope(scope)).digest()


def compute_nullifier(domain_secret: bytes, scope: str) -> bytes:
    if not domain_secret:
        raise ValueError("Domain secret must not be empty.")

    scope_hash = hash_scope(scope)
    return hmac.new(domain_secret, scope_hash, hashlib.sha256).digest()
