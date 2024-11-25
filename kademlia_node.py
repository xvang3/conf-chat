from kademlia.network import Server
import aiohttp

class KademliaNode:
    def __init__(self, port, boot_server_url="http://127.0.0.1:8468"):
        self.port = port
        self.server = Server()
        self.local_store = {}  # Local fallback storage
        self.boot_server_url = boot_server_url

    async def start(self, bootstrap_nodes=None):
        try:
            await self.server.listen(self.port)
            print(f"Node started on port {self.port}.")
            if bootstrap_nodes:
                await self.server.bootstrap(bootstrap_nodes)
                print(f"Bootstrapped to nodes: {bootstrap_nodes}")
            else:
                print("No bootstrap nodes provided; operating as standalone.")
        except Exception as e:
            print(f"Error starting server: {e}")
            self.server = None  # Explicitly set to None on failure



    async def set(self, key, value):
        if not self.server.protocol.router.find_neighbors(self.server.node):
            # Store on the boot server
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.boot_server_url}/set/{key}", json={"value": value}) as resp:
                    if resp.status == 200:
                        print(f"Stored key '{key}' on the boot server.")
                    else:
                        print(f"Failed to store key '{key}' on the boot server.")
        else:
            await self.server.set(key, value)

    async def get(self, key):
        if not self.server.protocol.router.find_neighbors(self.server.node):
            # Retrieve from the boot server
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.boot_server_url}/get/{key}") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"Retrieved key '{key}' from boot server: {data['value']}")
                        return data['value']
                    else:
                        print(f"Key '{key}' not found on the boot server.")
                        return None
        return await self.server.get(key)

    async def stop(self):
        if hasattr(self.server, "protocol") and hasattr(self.server.protocol, "transport") and self.server.protocol.transport:
            print("Stopping server...")
            try:
                await self.server.stop()  # Attempt a graceful stop
                print("Server stopped successfully.")
            except Exception as e:
                print(f"Error while stopping server gracefully: {e}")
        else:
            print("Server transport was not active or already stopped. Forcing cleanup...")
            # Force cleanup by manually setting attributes to None
            self.server.protocol = None
            self.server.transport = None
            print("Forced cleanup completed.")





