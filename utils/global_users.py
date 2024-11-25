import os
import json

GLOBAL_USERS_FILE = os.path.join(os.getcwd(), "users.json")

def ensure_global_users_file():
    """Ensure the global users.json file exists and is properly initialized."""
    if not os.path.exists(GLOBAL_USERS_FILE):
        # Create the file with an empty list if it doesn't exist
        with open(GLOBAL_USERS_FILE, "w") as f:
            json.dump([], f)
        print("Initialized global users.json file.")
    else:
        # Check if the file is empty or invalid, and fix it
        try:
            with open(GLOBAL_USERS_FILE, "r") as f:
                data = json.load(f)
            # If the file is not a list, reset it
            if not isinstance(data, list):
                raise ValueError
        except (json.JSONDecodeError, ValueError):
            with open(GLOBAL_USERS_FILE, "w") as f:
                json.dump([], f)
            print("Reinitialized corrupted global users.json file.")

def check_user_exists(username):
    """Check if a user exists in the global user list."""
    ensure_global_users_file()  # Ensure the file is ready
    with open(GLOBAL_USERS_FILE, "r") as f:
        users = json.load(f)
    return username in users

def add_to_global_users(username):
    """Add a username to the global user list."""
    ensure_global_users_file()  # Ensure the file is ready
    with open(GLOBAL_USERS_FILE, "r") as f:
        users = json.load(f)
    if username not in users:
        users.append(username)
        with open(GLOBAL_USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
        print(f"Added '{username}' to global users.")
    else:
        print(f"User '{username}' already exists.")
