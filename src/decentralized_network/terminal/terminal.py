
import asyncio

from decentralized_network import config
from decentralized_network.node import Node


class Terminal:
    
    node: Node
        
    def __init__(self):
        self.node = Node()
    
    
    async def run(self) -> None:
        
        while True:
            command = await asyncio.to_thread(input, config.TERMINAL_PROMPT)
            command = command.strip()
            
            if not command:
                continue
            
            if command in {"exit", "quit"}:
                break
            
            print(f"Unknown command: {command}")
