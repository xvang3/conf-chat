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
    """Add a user to the global users.json."""
    global_users_file = os.path.join(BASE_DIR, "users.json")

    # Ensure users.json exists
    if not os.path.exists(global_users_file):
        with open(global_users_file, "w") as f:
            json.dump([], f)

    # Load existing users
    with open(global_users_file, "r") as f:
        try:
            users = json.load(f)
            if not isinstance(users, list):
                raise ValueError("users.json must contain a list.")
        except (json.JSONDecodeError, ValueError):
            users = []

    # Add the new user if not already present
    if username not in users:
        users.append(username)
        with open(global_users_file, "w") as f:
            json.dump(users, f, indent=4)
        print(f"User '{username}' added to global users.")
    else:
        print(f"User '{username}' already exists in global users.")
