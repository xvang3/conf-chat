import asyncio
from kademlia_node import KademliaNode

async def test_kademlia():
    # Start the first node (bootstrap node) on port 8468
    first_node = KademliaNode(port=8468)
    await first_node.start()

    # Store a value in the first node
    await first_node.store("test_key", "test_value")
    print("Value stored in first node.")

    # Start a second node and bootstrap to the first node
    second_node = KademliaNode()
    await second_node.start(bootstrap_nodes=[("127.0.0.1", 8468)])

    # Retrieve the value from the second node
    retrieved_value = await second_node.retrieve("test_key")
    print(f"Retrieved value from second node: {retrieved_value}")

    # Stop the nodes
    await first_node.stop()
    await second_node.stop()

asyncio.run(test_kademlia())
