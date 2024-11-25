import os
import json
from kademlia.network import Server

class KademliaNode:
    def __init__(self, port=8468):
        self.port = port
        self.server = Server()  # Initialize Kademlia server

    async def start(self):
        await self.server.listen(self.port)

    async def store(self, key, value):
        await self.server.set(key, value)

    async def stop(self):
        self.server.stop()

