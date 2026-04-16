
import asyncio
from asyncio import AbstractServer, StreamReader, StreamWriter

from decentralized_network import config
from decentralized_network.personal import RootKeyRecord
from decentralized_network.personal import (
    create_named_root_key,
    fetch_root_key,
    fetch_root_secret,
)
from decentralized_network.services import (
    compute_service_nullifier,
    derive_service_nullifier_secret,
)

class Node:
    
    _root_key_record: RootKeyRecord | None
    _server: AbstractServer | None
    
    def __init__(self):
        self._root_key_record = None
        self._server = None
    
    @property
    def root_key_record(self) -> RootKeyRecord | None:
        return self._root_key_record

    @property
    def is_listening(self) -> bool:
        return self._server is not None

    async def start(self) -> None:
        if self._server is not None:
            return

        self._server = await asyncio.start_server(
            self._handle_connection,
            config.NODE_HOST,
            config.NODE_PORT,
        )

    async def stop(self) -> None:
        if self._server is None:
            return

        self._server.close()
        await self._server.wait_closed()
        self._server = None

    def listening_address(self) -> tuple[str, int] | None:
        if self._server is None or not self._server.sockets:
            return None

        host, port = self._server.sockets[0].getsockname()[:2]
        return host, port
    
    def create_named_root_key(self, name: str) -> RootKeyRecord:
        return create_named_root_key(name)
    
    def load_root_key(self, ref: int) -> RootKeyRecord | None:
        self._root_key_record = fetch_root_key(ref)
        return self.root_key_record

    def compute_service_nullifier(self, service_id_hex: str) -> bytes:
        if self._root_key_record is None:
            raise RuntimeError("No root key is currently loaded.")

        root_secret = fetch_root_secret(self._root_key_record.storage_ref)
        domain_secret = derive_service_nullifier_secret(root_secret)

        return compute_service_nullifier(domain_secret, service_id_hex)
    
    def clear_root_key_record(self) -> None:
        self._root_key_record = None

    async def _handle_connection(
        self,
        reader: StreamReader,
        writer: StreamWriter,
    ) -> None:
        writer.write(b"decentralized-network node\n")
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    
