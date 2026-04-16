
from decentralized_network.personal import RootKeyRecord
from decentralized_network.personal import create_named_root_key, fetch_root_key

class Node:
    
    _root_key_record: RootKeyRecord | None
    
    def __init__(self):
        self._root_key_record = None
    
    @property
    def root_key_record(self) -> RootKeyRecord | None:
        return self._root_key_record

    def create_named_root_key(self, name: str) -> RootKeyRecord:
        return create_named_root_key(name)
    
    def load_root_key(self, ref: int) -> RootKeyRecord | None:
        self._root_key_record = fetch_root_key(ref)
        return self.root_key_record
    
    def clear_root_key_record(self) -> None:
        self._root_key_record = None

    
