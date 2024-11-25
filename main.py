import asyncio
from kademlia_node import KademliaNode


async def main():
    # Determine if this is the first or second node
    role = determine_role()
    
    if role == "first":
        print("Starting the first node...")
        first_node = KademliaNode(port=8468)
        await first_node.start()
        print("First node started on port 8468.")

        # Store a key-value pair
        print("Storing a key-value pair on the first node...")
        await first_node.set("test_key", "test_value")
        print("Stored key: 'test_key', value: 'test_value'.")

        # Retrieve the key-value pair to verify storage
        print("Retrieving the key-value pair from the first node...")
        value = await first_node.get("test_key")
        print(f"Retrieved value for 'test_key' from the first node: {value}")

        print("Press Ctrl+C to exit the first node.")
        await asyncio.Future()  # Keep the first node running

    elif role == "second":
        print("Starting the second node...")
        second_node = KademliaNode(port=39059)
        first_node_ip = get_first_node_ip()
        await second_node.start(bootstrap_nodes=[(first_node_ip, 8468)])
        print(f"Second node started on port 39059 and bootstrapped to {first_node_ip}:8468.")

        # Retrieve the key-value pair from the first node
        print(f"Retrieving the key 'test_key' from the first node...")
        value = await second_node.get("test_key")
        print(f"Retrieved value for 'test_key' on the second node: {value}")

        print("Press Ctrl+C to exit the second node.")
        await asyncio.Future()  # Keep the second node running


def determine_role():
    """Determine the role of the node (first or second) based on port availability."""
    import socket
    try:
        # Try binding to port 8468 to check if the first node exists
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", 8468))
        sock.close()
        return "first"
    except OSError:
        return "second"


def get_first_node_ip():
    """Return the first node's IP address."""
    # Update this with the actual IP of the first VM
    return "127.0.0.1"  # Replace with actual VM IP for production


if __name__ == "__main__":
    asyncio.run(main())
