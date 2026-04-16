import json
from pathlib import Path

from decentralized_network import config


def read_root_key(storage_ref: int) -> dict:
    root_key_dir = Path(config.ROOT_KEY_PATH)
    if not root_key_dir.is_absolute():
        repo_root = Path(__file__).resolve().parents[4]
        root_key_dir = repo_root / root_key_dir

    root_key_path = root_key_dir / (
        f"{config.ROOT_KEY_NAME}{storage_ref}{config.ROOT_KEY_EXTENSION}"
    )

    return json.loads(root_key_path.read_text(encoding="utf-8"))
