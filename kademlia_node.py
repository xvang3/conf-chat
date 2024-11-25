import os
import json
from kademlia.network import Server

class KademliaNode:
    def __init__(self, port=8468):
        self.server = Server()
        self.port = port
        self.local_file = "users.json"

    async def start(self, bootstrap_nodes=None):
        await self.server.listen(self.port)
        if bootstrap_nodes:
            await self.server.bootstrap(bootstrap_nodes)
        if not os.path.exists(self.local_file):
            with open(self.local_file, "w") as f:
                json.dump({}, f)  # Create an empty users.json file

    async def stop(self):
        await self.server.stop()

    async def store(self, key, value):
        try:
            await self.server.set(key, value)
            if key.startswith("user:"):
                self.update_local_file(key, value)
        except Exception as e:
            print(f"Error storing key {key}: {e}")

    async def retrieve(self, key):
        try:
            value = await self.server.get(key)
            return value
        except Exception as e:
            print(f"Error retrieving key {key}: {e}")
            return None

    def update_local_file(self, key, value):
        if not key.startswith("user:"):
            return
        with open(self.local_file, "r") as f:
            data = json.load(f)
        data[key] = value
        with open(self.local_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_local_users(self):
        with open(self.local_file, "r") as f:
            return json.load(f)
