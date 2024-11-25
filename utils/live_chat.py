import zmq
import threading

def start_live_chat(username):
    """Start a simple peer-to-peer live chat session."""
    context = zmq.Context()

    # Ask user for port to listen on
    my_port = input("Enter your port to listen on (e.g., 6000): ").strip()
    my_address = f"tcp://*:{my_port}"
    print(f"Your chat address: tcp://localhost:{my_port}")

    # Create a socket to listen for incoming messages
    recv_socket = context.socket(zmq.REP)
    recv_socket.bind(my_address)

    # Start a thread to listen for incoming messages
    def listen_for_messages():
        while True:
            try:
                message = recv_socket.recv_json()
                sender = message.get("from", "Unknown")
                text = message.get("message", "")
                print(f"\n{sender}: {text}")
                recv_socket.send_json({"status": "received"})
            except zmq.ZMQError:
                break  # Exit when socket is closed

    listener_thread = threading.Thread(target=listen_for_messages, daemon=True)
    listener_thread.start()

    # Sending messages to a peer
    send_socket = context.socket(zmq.REQ)
    peer_address = input("Enter peer's chat address (e.g., tcp://localhost:6001): ").strip()

    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            print("Exiting live chat...")
            recv_socket.close()
            send_socket.close()
            break
        try:
            send_socket.connect(peer_address)
            send_socket.send_json({"from": username, "message": user_input})
            response = send_socket.recv_json()
            if response.get("status") == "received":
                print("Message delivered.")
            send_socket.disconnect(peer_address)
        except zmq.ZMQError as e:
            print(f"Error sending message: {e}")
