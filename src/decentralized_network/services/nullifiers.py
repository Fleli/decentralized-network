from decentralized_network.core.crypto.nullifiers import (
    compute_nullifier,
    derive_nullifier_domain_secret,
)


SERVICE_NULLIFIER_DOMAIN_LABEL = "service-id-nullifier:v1"
SERVICE_ID_NUM_BYTES = 32


def decode_service_id(service_id_hex: str) -> bytes:
    if not service_id_hex:
        raise ValueError("Service ID must not be empty.")

    try:
        service_id = bytes.fromhex(service_id_hex)
    except ValueError as exc:
        raise ValueError("Service ID must be valid hex.") from exc

    if len(service_id) != SERVICE_ID_NUM_BYTES:
        raise ValueError("Service ID must decode to exactly 32 bytes.")

    return service_id


def derive_service_nullifier_secret(root_secret: bytes) -> bytes:
    return derive_nullifier_domain_secret(root_secret, SERVICE_NULLIFIER_DOMAIN_LABEL)


def compute_service_nullifier(domain_secret: bytes, service_id_hex: str) -> bytes:
    service_id = decode_service_id(service_id_hex)
    return compute_nullifier(domain_secret, service_id.hex())
