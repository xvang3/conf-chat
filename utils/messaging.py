import json
import os
import zmq

def send_message(user_dir, recipient, message, sender):
    """Save a message to the sender's messages.json."""
    messages_file = os.path.join(user_dir, "messages.json")
    if not os.path.exists(messages_file):
        messages = {}
    else:
        with open(messages_file, "r") as f:
            messages = json.load(f)

    if recipient not in messages:
        messages[recipient] = []

    messages[recipient].append({"message": message, "from": sender})
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

def listen_for_messages(user_dir, listen_port):
    """Listen for real-time messages."""
    context = zmq.Context()
    recv_socket = context.socket(zmq.REP)
    recv_socket.bind(f"tcp://*:{listen_port}")

    while True:
        try:
            # Receive message
            message = recv_socket.recv_json()
            sender = message.get("from", "Unknown")
            text = message.get("message", "")
            print(f"\nReal-time message from {sender}: {text}")

            # Store the message locally
            messages_file = os.path.join(user_dir, "messages.json")
            if not os.path.exists(messages_file):
                messages = {}
            else:
                with open(messages_file, "r") as f:
                    messages = json.load(f)

            if sender not in messages:
                messages[sender] = []

            messages[sender].append({"message": text, "from": sender})
            with open(messages_file, "w") as f:
                json.dump(messages, f, indent=4)

            # Acknowledge receipt
            recv_socket.send_json({"status": "received"})
        except zmq.ZMQError:
            print("Error receiving message.")
            break

