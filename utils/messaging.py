import json
import os

def send_message(user_dir, recipient, message):
    messages_file = os.path.join(user_dir, "messages.json")
    if not os.path.exists(messages_file):
        messages = {}
    else:
        with open(messages_file, "r") as f:
            messages = json.load(f)

    if recipient not in messages:
        messages[recipient] = []

    messages[recipient].append({"message": message, "from": "you"})
    with open(messages_file, "w") as f:
        json.dump(messages, f, indent=4)

    print(f"Message sent to {recipient}.")

def receive_messages(user_dir):
    messages_file = os.path.join(user_dir, "messages.json")
    if not os.path.exists(messages_file):
        print("No messages found.")
        return

    with open(messages_file, "r") as f:
        messages = json.load(f)

    for sender, msgs in messages.items():
        print(f"\nMessages from {sender}:")
        for msg in msgs:
            print(f"  - {msg['message']}")

    print("All messages displayed.")
