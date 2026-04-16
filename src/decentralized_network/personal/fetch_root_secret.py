from .storage import read_root_key


def fetch_root_secret(storage_ref: int) -> bytes:
    payload = read_root_key(storage_ref)
    return bytes.fromhex(payload["root_key_hex"])
