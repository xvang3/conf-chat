# main.py
import asyncio
from kademlia_node import KademliaNode

async def main():
    # Start the first node
    first_node = KademliaNode(port=8468)
    await first_node.start()
    print(f"First node started on port {first_node.port}.")

    # Store a key-value pair
    await first_node.store("test_key", "test_value")
    print("Stored key 'test_key' with value 'test_value'.")

    # Stop the first node
    await first_node.stop()

if __name__ == "__main__":
    asyncio.run(main())

