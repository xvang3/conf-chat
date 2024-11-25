import asyncio
from kademlia.network import Server
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

async def run_bootstrap_server():
    print("Starting the bootstrap server on port 8468...")
    server = Server()
    await server.listen(8468)
    print("Bootstrap server is running on port 8468.")
    print("Press Ctrl+C to stop the server.")

    try:
        await asyncio.Future()  # Keep the server running
    except asyncio.CancelledError:
        print("Stopping bootstrap server...")
        await server.stop()

if __name__ == "__main__":
    asyncio.run(run_bootstrap_server())
