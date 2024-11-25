from kademlia.network import Server

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
            # Retrieve locally if no neighbors
            print(f"Retrieving locally: {key}")
            return self.local_store.get(key)
        return await self.server.get(key)

    async def stop(self):
        if self.server.transport:
            await self.server.stop()
