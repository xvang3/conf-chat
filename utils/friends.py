import os
import json

GLOBAL_USERS_FILE = os.path.join(os.getcwd(), "users.json")

def ensure_global_users_file():
    """Ensure the global users.json file exists."""
    if not os.path.exists(GLOBAL_USERS_FILE):
        with open(GLOBAL_USERS_FILE, "w") as f:
            json.dump([], f)

def add_to_global_users(username):
    """Add a new user to the global users.json file."""
    ensure_global_users_file()
    with open(GLOBAL_USERS_FILE, "r") as f:
        users = json.load(f)
    
    if username not in users:
        users.append(username)
        with open(GLOBAL_USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)

def check_user_exists(username):
    """Check if a username exists in the global users.json file."""
    ensure_global_users_file()
    with open(GLOBAL_USERS_FILE, "r") as f:
        users = json.load(f)
    return username in users

def initialize_friends_file(user_dir):
    """Initialize the friends.json file if it doesn't exist."""
    friends_file = os.path.join(user_dir, "friends.json")
    if not os.path.exists(friends_file):
        with open(friends_file, "w") as f:
            json.dump([], f)

from utils.global_users import check_user_exists

def add_friend(user_dir, friend):
    """Add a friend to the user's friends list."""
    friends_file = os.path.join(user_dir, "friends.json")

    # Load the current friends list
    if not os.path.exists(friends_file):
        friends = []
    else:
        with open(friends_file, "r") as f:
            try:
                friends = json.load(f)
                if not isinstance(friends, list):
                    raise ValueError("Invalid friends.json format")
            except (json.JSONDecodeError, ValueError):
                print("Error reading friends list. Reinitializing...")
                friends = []

    # Check if the friend is already in the list
    if friend in friends:
        print(f"{friend} is already your friend.")
        return

    # Check if the friend exists globally
    if not check_user_exists(friend):
        print(f"User '{friend}' does not exist.")
        return

    # Add the friend and save the updated list
    friends.append(friend)
    with open(friends_file, "w") as f:
        json.dump(friends, f, indent=4)
    print(f"Added {friend} as a friend.")


def remove_friend(user_dir, friend):
    """Remove a friend from the user's friends list."""
    initialize_friends_file(user_dir)

    friends_file = os.path.join(user_dir, "friends.json")
    with open(friends_file, "r") as f:
        friends = json.load(f)

    if friend not in friends:
        print(f"{friend} is not your friend.")
        return

    friends.remove(friend)
    with open(friends_file, "w") as f:
        json.dump(friends, f, indent=4)

    print(f"{friend} has been removed from your friends list.")

def list_all_friends(user_dir, current_user):
    """List all friends of the logged-in user, excluding the user themselves."""
    friends_file = os.path.join(user_dir, "friends.json")
    if not os.path.exists(friends_file):
        print("You have no friends yet.")
        return

    try:
        with open(friends_file, "r") as f:
            friends = json.load(f)
            if not isinstance(friends, list):
                raise ValueError("Invalid friends.json format")
    except (json.JSONDecodeError, ValueError):
        print("Error reading friends list.")
        return

    friends = [friend for friend in friends if friend != current_user]

    if not friends:
        print("You have no friends yet.")
    else:
        print("Your friends:")
        for friend in friends:
            print(f"- {friend}")    


