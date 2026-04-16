from datetime import datetime

from .root_key_record import RootKeyRecord
from .storage import read_root_key


def fetch_root_key(storage_ref: int) -> RootKeyRecord:
    payload = read_root_key(storage_ref)
    created_at = datetime.fromisoformat(payload["created_at"])

    return RootKeyRecord(payload["name"], created_at, storage_ref)
