from kademlia.network import Server
import aiohttp

class KademliaNode:
    def __init__(self, port):
        self.port = port
        self.server = Server()
        self.local_store = {}  # Local storage for standalone nodes

    async def start(self, bootstrap_nodes=None):
        await self.server.listen(self.port)
        if bootstrap_nodes:
            await self.server.bootstrap(bootstrap_nodes)

    async def set(self, key, value):
        if not self.server.protocol.router.find_neighbors(self.server.node):
            # If no neighbors, store locally
            self.local_store[key] = value
            print(f"Storing locally: {key} -> {value}")
        else:
            await self.server.set(key, value)

    async def get(self, key):
        if not self.server.protocol.router.find_neighbors(self.server.node):
            # Query the standalone server as a fallback
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http:10.138.0.5:8468/get/{key}") as resp:
                    if resp.status == 200:
                        return await resp.text()
            print(f"No neighbors and no response from standalone server for: {key}")
            return None
        return await self.server.get(key)


    async def stop(self):
        if self.server.transport:
            await self.server.stop()
