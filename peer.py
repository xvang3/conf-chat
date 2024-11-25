import random
from utils.sync_manager import *
from user_directory import *

class Peer:
    def __init__(self, username, address):
        self.username = username
        self.address = address
        self.user_directory = UserDirectory(username)
        self.sync_manager = SyncManager(self.user_directory)

    def connect_to_peer(self, peer_address):
        # Simulate retrieving data from the peer
        print(f"Connecting to peer at {peer_address}...")
        peer_data = self.simulate_peer_data()
        self.sync_manager.sync_data(peer_data)

    def simulate_peer_data(self):
        # Simulated peer data for testing
        return {
            "username": self.username,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "data": {
                "messages": [f"Message from peer {random.randint(1, 100)}"],
                "peers": [f"peer_{random.randint(1, 100)}"]
            }
        }
