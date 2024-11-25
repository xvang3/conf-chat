from file_utils import *

def send_message(sender, recipient, content):
    data = load_data()

    # Ensure both users exist
    if sender not in data:
        print(f"Error: Sender '{sender}' does not exist.")
        return
    if recipient not in data:
        print(f"Error: Recipient '{recipient}' does not exist.")
        return

    # Ensure the recipient is a friend
    if recipient not in data[sender].get("friends", []):
        print(f"Error: '{recipient}' is not your friend.")
        return

    # Add the message
    if add_message(recipient, sender, content):
        print(f"Message sent to '{recipient}'.")
    else:
        print("Failed to send message.")

def retrieve_messages(username):
    data = load_data()

    # Check if user exists
    if username not in data:
        print(f"Error: User '{username}' does not exist.")
        return

    # Get messages
    messages = data[username].get("messages", [])
    if not messages:
        print("No new messages.")
    else:
        print(f"Messages for {username}:")
        for msg in messages:
            print(f"[{msg['timestamp']}] {msg['sender']}: {msg['content']}")

    # Clear messages after retrieval
    update_user(username, "messages", [])
