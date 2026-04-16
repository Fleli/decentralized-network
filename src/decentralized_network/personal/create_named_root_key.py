
from datetime import datetime

from decentralized_network.core.crypto import generate_root_key

from .root_key_record import RootKeyRecord
from .storage import save_root_key

def create_named_root_key(name: str) -> RootKeyRecord:
    key = generate_root_key()
    now = datetime.now()
    ref = save_root_key(name, key, now)

    return RootKeyRecord(name, now, ref)
    
