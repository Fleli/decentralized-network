
from datetime import datetime

class RootKeyRecord():
    
    name: str
    created_at: datetime
    storage_ref: int
    
    def __init__(self, name: str, created_at: datetime, storage_ref: int):
        self.name = name
        self.created_at = created_at
        self.storage_ref = storage_ref
