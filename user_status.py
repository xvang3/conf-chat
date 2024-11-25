from file_utils import *

# In-memory set to track online users
online_users = set()

async def login_user(username, kademlia_node):
    """Mark a user as online in the DHT."""
    key = f"{username}:status"
    await kademlia_node.store(key, "online")
    print(f"'{username}' is now online.")

async def logout_user(username, kademlia_node):
    """Mark a user as offline in the DHT."""
    key = f"{username}:status"
    await kademlia_node.store(key, "offline")
    print(f"'{username}' is now offline.")

async def is_user_online(username, kademlia_node):
    """Check if a user is online."""
    key = f"{username}:status"
    status = await kademlia_node.retrieve(key)
    return status == "online"

