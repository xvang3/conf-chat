import logging
from kademlia_node import KademliaNode
import asyncio

# Configure logging to show all DEBUG messages in the terminal
logging.basicConfig(
    level=logging.DEBUG,  # Log everything from DEBUG level and above
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',  # Timestamp and log details
    datefmt='%Y-%m-%d %H:%M:%S'  # Human-readable timestamps
)

async def main():
    logging.info("Starting node...")
    # Initialize and start your node here
    first_node = KademliaNode(8468)
    await first_node.start()
    logging.info("Node started successfully.")
    # Your main program logic
    await first_node.set("test_key", "test_value")
    logging.info("Key set: test_key -> test_value")
    retrieved = await first_node.get("test_key")
    logging.info(f"Retrieved value for 'test_key': {retrieved}")
    await first_node.stop()
    logging.info("Node stopped.")

if __name__ == "__main__":
    asyncio.run(main())
