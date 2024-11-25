import json
import os
from datetime import datetime


DATA_FILE = "users.json"

def load_data():
    """Load user data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    """Save user data to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_user(username, field, value):
    """Update a specific field for a user in the JSON file."""
    data = load_data()
    if username in data:
        data[username][field] = value
        save_data(data)
        return True
    return False

def add_message(recipient, sender, content):
    """Add a message to the recipient's messages field."""
    data = load_data()

    # Ensure recipient exists
    if recipient not in data:
        print(f"Error: Recipient '{recipient}' does not exist.")
        return False

    # Add the message
    messages = data[recipient].get("messages", [])
    messages.append({
        "sender": sender,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    update_user(recipient, "messages", messages)
    return True

def add_request(username, requester):
    """Add a friend request to a user's requests field."""
    data = load_data()

    if username not in data:
        print(f"Error: User '{username}' does not exist.")
        return False

    # Add the request if it doesn't already exist
    requests = data[username].get("requests", [])
    if requester in requests:
        print(f"Error: '{requester}' already sent a request to '{username}'.")
        return False

    requests.append(requester)
    update_user(username, "requests", requests)
    return True

def remove_request(username, requester):
    """Remove a friend request from a user's requests field."""
    data = load_data()

    if username not in data:
        print(f"Error: User '{username}' does not exist.")
        return False

    requests = data[username].get("requests", [])
    if requester not in requests:
        print(f"Error: No request from '{requester}' to '{username}'.")
        return False

    requests.remove(requester)
    update_user(username, "requests", requests)
    return True

def normalize_username(username):
    """Convert a username to lowercase to ensure case-insensitivity."""
    return username.strip().lower()
