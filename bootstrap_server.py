import asyncio
from kademlia.network import Server
import logging

class BootstrapServer:
    def __init__(self, port=8468):
        self.port = port
        self.server = Server()
        self.local_store = {}  # Fallback dictionary for key-value storage

    async def start(self):
        await self.server.listen(self.port)
        print(f"Bootstrap server started on port {self.port}")
        while True:
            await asyncio.sleep(3600)  # Keep the server running

    async def set_local(self, key, value):
        self.local_store[key] = value
        print(f"Stored locally: {key} -> {value}")

    async def get_local(self, key):
        value = self.local_store.get(key, None)
        print(f"Retrieved locally: {key} -> {value}")
        return value

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    bootstrap_server = BootstrapServer()

    asyncio.run(bootstrap_server.start())
