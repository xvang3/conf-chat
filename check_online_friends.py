from file_utils import *
from friend_management import *

def check_online_friends(username):
    """Check which of a user's friends are online."""
    username = normalize_username(username)
    data = load_data()

    if username not in data:
        print(f"Error: User '{username}' does not exist.")
        return

    friends = [normalize_username(friend) for friend in data[username].get("friends", [])]

    if not friends:
        print("You have no friends.")
        return

    online_friends = [friend for friend in friends if data.get(friend, {}).get("online", False)]
    offline_friends = [friend for friend in friends if friend not in online_friends]

    print(f"Online friends: {', '.join(online_friends) if online_friends else 'None'}")
    print(f"Offline friends: {', '.join(offline_friends) if offline_friends else 'None'}")

