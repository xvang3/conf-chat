from file_utils import *

# In-memory set to track online users
online_users = set()

def login_user(username):
    """Mark a user as online."""
    username = normalize_username(username)  # Normalize username
    online_users.add(username)
    print(f"'{username}' is now online.")

def logout_user(username):
    """Mark a user as offline."""
    username = normalize_username(username)  # Normalize username
    if username in online_users:
        online_users.remove(username)
        print(f"'{username}' is now offline.")
    else:
        print(f"Error: '{username}' was not logged in.")

def is_user_online(username):
    """Check if a user is online."""
    username = normalize_username(username)  # Normalize username
    return username in online_users
