from kademlia.network import Server


class KademliaNode:
    def __init__(self, port):
        self.port = port
        self.server = Server()

    async def start(self, bootstrap_nodes=None):
        await self.server.listen(self.port)
        if bootstrap_nodes:
            await self.server.bootstrap(bootstrap_nodes)

    async def set(self, key, value):
        print(f"Storing key: {key}, value: {value}")
        await self.server.set(key, value)

    async def get(self, key):
        print(f"Retrieving key: {key}")
        return await self.server.get(key)

    async def stop(self):
        await self.server.stop()
