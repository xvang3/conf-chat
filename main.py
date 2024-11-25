async def main():
    node_type = input("Is this the first node? (yes/no): ").strip().lower()
    if node_type == "yes":
        # First node
        first_node = KademliaNode(8468)
        await first_node.start()
        print("First node started on port 8468.")
        await first_node.set("test_key", "test_value")
        print("Stored key: 'test_key', value: 'test_value'")
        retrieved_value = await first_node.get("test_key")
        print(f"Retrieved value for 'test_key': {retrieved_value}")
        await first_node.stop()
    else:
        # Second node
        second_node = KademliaNode(39059)
        bootstrap_nodes = [("10.138.0.2", 8468)]  # Replace with actual bootstrap node IPs
        await second_node.start(bootstrap_nodes=bootstrap_nodes)
        print("Second node started on port 39059.")
        retrieved_value = await second_node.get("test_key")
        print(f"Retrieved value for 'test_key' from bootstrap node: {retrieved_value}")
        await second_node.stop()
