import zmq
import threading

def start_live_chat(username, user_dir):
    """Start a simplified peer-to-peer live chat session."""
    context = zmq.Context()

    # Ask user for port to listen on
    my_port = input("Enter your port to listen on (e.g., 6000): ").strip()
    my_address = f"tcp://*:{my_port}"
    print(f"Your chat address: tcp://localhost:{my_port}")

    # Create a socket to listen for incoming messages
    recv_socket = context.socket(zmq.REP)
    try:
        recv_socket.bind(my_address)
    except zmq.ZMQError as e:
        print(f"Error binding to port {my_port}: {e}")
        return

    # Start a thread to listen for incoming messages
    def listen_for_messages():
        while True:
            try:
                message = recv_socket.recv_json(flags=zmq.NOBLOCK)
                sender = message.get("from", "Unknown")
                text = message.get("message", "")
                print(f"\n{sender}: {text}")
                recv_socket.send_json({"status": "received"})
            except zmq.Again:
                pass  # Non-blocking mode: no messages yet
            except zmq.ZMQError:
                break  # Exit when socket is closed

    listener_thread = threading.Thread(target=listen_for_messages, daemon=True)
    listener_thread.start()

    # Load friends and their corresponding ports
    friends = load_user_data(user_dir, "friends.json")  # Assume it stores {username: port}
    if not isinstance(friends, dict):
        print("No valid friends data found.")
        friends = {}

    # Sending messages to a peer
    send_socket = context.socket(zmq.REQ)

    print("Type 'list' to see online friends, 'exit' to quit.")
    while True:
        recipient = input("Enter friend's name or port (e.g., alice or 6001): ").strip()
        if recipient.lower() == "exit":
            print("Exiting live chat...")
            recv_socket.close()
            send_socket.close()
            break
        elif recipient.lower() == "list":
            print("Online friends:")
            for friend, port in friends.items():
                print(f"{friend}: {port}")
            continue

        # Check if recipient is a name or port
        peer_address = None
        if recipient in friends:
            peer_address = f"tcp://localhost:{friends[recipient]}"
        elif recipient.isdigit():
            peer_address = f"tcp://localhost:{recipient}"

        if not peer_address:
            print(f"Unknown recipient: {recipient}")
            continue

        try:
            send_socket.connect(peer_address)
            user_input = input("> ").strip()
            send_socket.send_json({"from": username, "message": user_input})
            response = send_socket.recv_json()
            if response.get("status") == "received":
                print("Message delivered.")
            send_socket.disconnect(peer_address)  # Disconnect to allow reconnect if needed
        except zmq.ZMQError as e:
            print(f"Error sending message: {e}")


