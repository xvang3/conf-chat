import os
import json
import shutil
import requests

SERVER_ADDRESS = "http://localhost:5555"

def sync_with_peer_or_server(user_dir):
    """Synchronize peer data with the server."""
    # Load local data for synchronization
    local_data = {
        "friends": load_user_data(user_dir, "friends.json"),
        "messages": load_user_data(user_dir, "messages.json"),
    }

    try:
        # Fetch data from the server
        response = requests.get(f"{SERVER_ADDRESS}/sync")
        if response.status_code == 200:
            try:
                server_data = response.json()
            except json.JSONDecodeError:
                print("Failed to parse server response. Sync aborted.")
                return False

            # Merge local and server data
            merged_data = {
                "friends": merge_lists(local_data["friends"], server_data.get("friends", [])),
                "messages": merge_dicts(local_data["messages"], server_data.get("messages", {})),
            }

            # Save merged data locally
            save_user_data(user_dir, "friends.json", merged_data["friends"])
            save_user_data(user_dir, "messages.json", merged_data["messages"])

            # Push merged data back to the server
            sync_response = requests.post(f"{SERVER_ADDRESS}/sync", json=merged_data)
            if sync_response.status_code == 200:
                print("Synchronized user data successfully.")
                return True
            else:
                print(f"Failed to push merged data to server: {sync_response.json().get('error', 'Unknown error')}")
        else:
            print(f"Failed to fetch server data. Status code: {response.status_code}")
    except requests.ConnectionError as e:
        print(f"Connection error during sync: {e}")

    return False




def merge_lists(local, remote):
    """Merge two lists without duplicates."""
    return list(set(local) | set(remote))

def merge_dicts(local, remote):
    """Merge two dictionaries with priority for the most recent changes."""
    merged = local.copy()
    merged.update(remote)  # Assumes remote is the authoritative source
    return merged

def load_user_data(user_dir, file_name):
    """Load user data from a specific file in the user's directory."""
    file_path = os.path.join(user_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Error reading {file_name}. Reinitializing file.")
                with open(file_path, "w") as reset_file:
                    json.dump([], reset_file) if "friends" in file_name else json.dump({}, reset_file)
                return []
    return [] if "friends" in file_name else {}

def save_user_data(user_dir, file_name, data):
    """Save user data to a specific file in the user's directory."""
    file_path = os.path.join(user_dir, file_name)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)