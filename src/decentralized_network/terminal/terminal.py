
import asyncio

from decentralized_network import config
from decentralized_network.node import Node


class Terminal:
    
    node: Node
    
    def __init__(self):
        self.node = Node()
    
    
    async def run(self) -> None:
        
        print("\nStarting node ...")
        
        await self.node.start()
        
        address = self.node.listening_address()
        
        if address is not None:
            print(f"Node listening on {address[0]}:{address[1]}")
        
        print("")
        
        try:
            while True:
                command = await asyncio.to_thread(input, config.TERMINAL_PROMPT)
                command = command.strip()
                
                if not command:
                    continue
                
                if command in {"exit", "quit"}:
                    break
                
                if command.startswith("create "):
                    name = command.removeprefix("create ").strip()
                    if not name:
                        print("Usage: create <name>")
                        continue

                    record = self.node.create_named_root_key(name)
                    print(
                        f"Created root key '{record.name}' with ref {record.storage_ref}."
                    )
                    continue
                
                if command.startswith("load "):
                    ref_text = command.removeprefix("load ").strip()
                    if not ref_text:
                        print("Usage: load <ref>")
                        continue
                    
                    try:
                        ref = int(ref_text)
                        record = self.node.load_root_key(ref)
                    except ValueError:
                        print("Root key ref must be an integer.")
                        continue
                    except FileNotFoundError:
                        print(f"No root key found for ref {ref_text}.")
                        continue
                    
                    print(f"Loaded root key '{record.name}' with ref {record.storage_ref}.")
                    continue
                
                print(f"Unknown command: {command}")
        finally:
            print("\nStopping node gracefully ...\n")
            await self.node.stop()
