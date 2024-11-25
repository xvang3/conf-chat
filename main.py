# main.py
import asyncio
from kademlia_node import KademliaNode

async def main():
    first_node = KademliaNode(port=8468)
    await first_node.start()
    print("First node started on port 8468.")

    await first_node.set("test_key", "test_value")
    print("Stored 'test_key': 'test_value' on first node.")

    # Use the public IP of the first VM for bootstrapping
    second_node = KademliaNode(port=39059)
    await second_node.start(bootstrap_nodes=[("FIRST_NODE_PUBLIC_IP", 8468)])
    print("Second node started on port 39059 and bootstrapped to first node.")

    retrieved_value = await second_node.get("test_key")
    print("Retrieved from second node:", retrieved_value)

    await asyncio.sleep(5)
    await first_node.stop()
    await second_node.stop()

if __name__ == "__main__":
    asyncio.run(main())
