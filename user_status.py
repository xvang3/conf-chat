from file_utils import *

# In-memory set to track online users
online_users = set()

def login_user(username):
    """Mark a user as online."""
    username = normalize_username(username)
    data = load_data()

    if username in data:
        data[username]["online"] = True  # Set user as online
        save_data(data)
        print(f"'{username}' is now online.")
    else:
        print(f"Error: User '{username}' does not exist.")

def logout_user(username):
    """Mark a user as offline."""
    username = normalize_username(username)
    data = load_data()

    if username in data:
        data[username]["online"] = False  # Set user as offline
        save_data(data)
        print(f"'{username}' is now offline.")
    else:
        print(f"Error: User '{username}' does not exist.")

def is_user_online(username):
    """Check if a user is online."""
    username = normalize_username(username)
    data = load_data()
    return data.get(username, {}).get("online", False)
