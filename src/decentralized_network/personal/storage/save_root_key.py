import json
from datetime import datetime
from pathlib import Path

from decentralized_network import config


def save_root_key(name: str, root_key: bytes, created_at: datetime) -> int:
    if not name:
        raise ValueError("Root key name must not be empty.")

    if not root_key:
        raise ValueError("Root key must not be empty.")

    root_key_dir = Path(config.ROOT_KEY_PATH)
    if not root_key_dir.is_absolute():
        repo_root = Path(__file__).resolve().parents[4]
        root_key_dir = repo_root / root_key_dir

    root_key_dir.mkdir(parents=True, exist_ok=True)

    storage_ref = 0
    root_key_path = root_key_dir / (
        f"{config.ROOT_KEY_NAME}{storage_ref}{config.ROOT_KEY_EXTENSION}"
    )
    while root_key_path.exists():
        storage_ref += 1
        root_key_path = root_key_dir / (
            f"{config.ROOT_KEY_NAME}{storage_ref}{config.ROOT_KEY_EXTENSION}"
        )

    payload = {
        "name": name,
        "created_at": created_at.isoformat(),
        "root_key_hex": root_key.hex(),
    }
    root_key_path.write_text(json.dumps(payload), encoding="utf-8")

    return storage_ref
