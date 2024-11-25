from file_utils import *
from user_status import *

def add_friend(username, friend_username):
    data = load_data()

    # Check if the user and friend exist
    if username not in data:
        print(f"Error: User '{username}' does not exist.")
        return
    if friend_username not in data:
        print(f"Error: Friend '{friend_username}' does not exist.")
        return

    # Prevent adding self or duplicates
    if username == friend_username:
        print("Error: You cannot add yourself as a friend.")
        return
    if friend_username in data[username].get("friends", []):
        print(f"Error: '{friend_username}' is already your friend.")
        return

    # Add friend
    friends = data[username].get("friends", [])
    friends.append(friend_username)
    update_user(username, "friends", friends)
    print(f"'{friend_username}' added as a friend.")

def remove_friend(username, friend_username):
    data = load_data()

    # Check if the user exists
    if username not in data:
        print(f"Error: User '{username}' does not exist.")
        return

    # Check if the friend is in the user's friend list
    friends = data[username].get("friends", [])
    if friend_username not in friends:
        print(f"Error: '{friend_username}' is not in your friend list.")
        return

    # Remove friend
    friends.remove(friend_username)
    update_user(username, "friends", friends)
    print(f"'{friend_username}' removed from your friend list.")

def view_friend_requests(username):
    username = normalize_username(username)
    data = load_data()

    if username not in data:
        print(f"Error: User '{username}' does not exist.")
        return

    requests = data[username].get("requests", [])
    if not requests:
        print("No friend requests.")
    else:
        print("Friend requests:", ", ".join(requests))


def send_friend_request(sender, recipient):
    sender = normalize_username(sender)
    recipient = normalize_username(recipient)

    if sender == recipient:
        print("Error: You cannot send a request to yourself.")
        return

    if add_request(recipient, sender):
        print(f"Friend request sent to '{recipient}'.")
    else:
        print("Failed to send friend request.")

def accept_friend_request(username, requester):
    username = normalize_username(username)
    requester = normalize_username(requester)

    data = load_data()

    if username not in data:
        print(f"Error: User '{username}' does not exist.")
        return
    if requester not in data:
        print(f"Error: User '{requester}' does not exist.")
        return

    if not remove_request(username, requester):
        print(f"Error: No friend request from '{requester}'.")
        return

    user_friends = data[username].get("friends", [])
    requester_friends = data[requester].get("friends", [])

    if requester not in user_friends:
        user_friends.append(requester)
    if username not in requester_friends:
        requester_friends.append(username)

    update_user(username, "friends", user_friends)
    update_user(requester, "friends", requester_friends)
    print(f"'{username}' and '{requester}' are now friends!")

def reject_friend_request(username, requester):
    """Reject a friend request."""
    if remove_request(username, requester):
        print(f"Friend request from '{requester}' rejected.")
    else:
        print(f"Error: No friend request from '{requester}'.")

def view_friends(username):
    data = load_data()

    # Check if the user exists
    if username not in data:
        print(f"Error: User '{username}' does not exist.")
        return

    # Display friends
    friends = data[username].get("friends", [])
    if not friends:
        print("You have no friends.")
    else:
        print("Your friends:", ", ".join(friends))


