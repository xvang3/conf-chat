import asyncio
import sys
from kademlia_node import KademliaNode

async def main():
    # Determine if this is the first, second, or third node
    node_port = 8468 if "second" not in sys.argv and "third" not in sys.argv else (39059 if "second" in sys.argv else 49059)
    bootstrap_nodes = None

    if "second" in sys.argv:
        # Second node bootstraps to the first node
        bootstrap_nodes = [("10.138.0.2", 8468)]  # First node internal IP and port
    elif "third" in sys.argv:
        # Third node bootstraps to the second node
        bootstrap_nodes = [("10.138.0.3", 39059)]  # Second node internal IP and port

    # Start the node
    print(f"Starting node on port {node_port}...")
    node = KademliaNode(node_port)
    await node.start(bootstrap_nodes=bootstrap_nodes)

    if not bootstrap_nodes:
        # First node: Store a test key-value pair
        print("Storing a key-value pair on the first node...")
        await node.set("test_key", "test_value")
        print("Stored key: 'test_key', value: 'test_value'.")
    else:
        # Other nodes: Retrieve the key-value pair
        print(f"Retrieving the key-value pair from the bootstrap node...")
        retrieved_value = await node.get("test_key")
        print(f"Retrieved value for 'test_key': {retrieved_value}")

    # Keep the node running
    print("Press Ctrl+C to exit.")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down node...")
        await node.stop()

if __name__ == "__main__":
    asyncio.run(main())
