import os
import json
import zmq
from utils.sync_manager import sync_with_peer_or_server
from utils.messaging import send_message, receive_messages
from utils.friends import *
from utils.friends import add_to_global_users
from utils.global_users import ensure_global_users_file
import threading
from utils.live_chat import start_live_chat
import requests
from server import *




ensure_global_users_file()

BASE_DIR = os.path.join(os.getcwd(), "users")
SERVER_ADDRESS = "http://localhost:5555"
SERVER_ADDRESS = SERVER_ADDRESS.replace("tcp://", "http://")


def ensure_base_directory():
    """Ensure the base directory for storing user data exists."""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        print(f"Created base directory: {BASE_DIR}")

ensure_base_directory()

# Function to start the node in the background
def run_node():
    """Run the node in a background thread."""
    node_socket, node_port = start_node()
    print(f"Node started and listening on {node_port}.")

    # Keep the node alive to listen for incoming P2P messages
    while True:
        try:
            message = node_socket.recv_json()
            print(f"Node: Received message -> {message}")
            node_socket.send_json({"status": "received", "message": "Acknowledged"})
        except zmq.ZMQError as e:
            print(f"Node error: {e}")
            break

def create_user_directory(username):
    user_dir = os.path.join(BASE_DIR, username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
        print(f"Created user directory: {user_dir}")
        for file_name in ["user_data.json", "messages.json", "friends.json", "group_chats.json"]:
            with open(os.path.join(user_dir, file_name), "w") as f:
                f.write("{}")
    return user_dir


def load_user_data(user_dir, file_name):
    """Load data from a user's file."""
    file_path = os.path.join(user_dir, file_name)
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_data(user_dir, file_name, data):
    """Save data to a user's file."""
    file_path = os.path.join(user_dir, file_name)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def find_available_server_port(base_port=6000, max_attempts=100):
    context = zmq.Context()
    for port in range(base_port, base_port + max_attempts):
        try:
            socket = context.socket(zmq.REP)
            socket.bind(f"tcp://*:{port}")
            socket.close()
            return f"tcp://localhost:{port}"
        except zmq.ZMQError:
            continue
    print("No available port found.")
    return None

def register():
    """Register a new user."""
    username = input("Enter a username: ").strip()
    password = input("Enter a password: ").strip()

    # Create user directory
    user_dir = create_user_directory(username)

    # Load existing user data
    user_data = load_user_data(user_dir, "user_data.json")

    # Check if the user already exists
    if "password" in user_data:
        print("User already exists.")
        return

    # Save user credentials
    user_data["password"] = password
    save_user_data(user_dir, "user_data.json", user_data)

    # Add the user to global users.json
    try:
        add_to_global_users(username)
        print(f"User {username} registered successfully.")
    except Exception as e:
        print(f"Failed to register user: {e}")


def login():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    user_dir = os.path.join(BASE_DIR, username)
    if not os.path.exists(user_dir):
        print(f"User {username} does not exist.")
        return

    with open(os.path.join(user_dir, "user_data.json"), "r") as f:
        user_data = json.load(f)

    if user_data.get("password") != password:
        print("Incorrect password.")
        return

    print(f"Welcome back, {username}!")

    # Synchronize in a separate thread
    sync_thread = threading.Thread(target=sync_with_peer_or_server, args=(user_dir,), daemon=True)
    sync_thread.start()

    logged_in_menu(username, user_dir)



def check_friends_status(user_dir, current_user):
    """Check the online/offline status of the user's friends."""
    friends = load_user_data(user_dir, "friends.json")
    if not friends:
        print("You have no friends yet.")
        return

    try:
        # Read online users from shared file
        with open("server_data/online_users.json", "r") as f:
            online_users = json.load(f)

        print("Friend status:")
        for friend in friends:
            if friend == current_user:
                continue
            if friend in online_users:
                print(f"{friend}: Online")
            else:
                print(f"{friend}: Offline")
    except FileNotFoundError:
        print("No online users data available.")
    except json.JSONDecodeError:
        print("Error reading online users data.")











    SERVER_STATUS_URL = f"{SERVER_ADDRESS}/user_status"

    def update_user_status(username, action):
        """Notify the server of the user's status (login/logout)."""
        try:
            response = requests.post(SERVER_STATUS_URL, json={"username": username, "action": action})
            if response.status_code == 200:
                print(response.json().get("message"))
            else:
                print(f"Failed to update user status: {response.text}")
        except requests.RequestException as e:
            print(f"Error communicating with server: {e}")

def discover_peers(port_range=(6000, 6010)):
    """Discover active peers in the given port range."""
    peers = []
    for port in range(*port_range):
        peer_address = f"http://localhost:{port}"
        try:
            response = requests.get(f"{peer_address}/ping")
            if response.status_code == 200:
                peers.append(peer_address)
        except requests.RequestException:
            continue  # Ignore unreachable peers
    return peers


def live_chat(user_dir, username):
    """Start a live chat session."""
    import threading
    context = zmq.Context()

    # Assign a port for the current user
    user_port = find_available_server_port(base_port=6000, max_attempts=100)
    if not user_port:
        print("No available port for live chat.")
        return

    chat_socket = context.socket(zmq.REP)
    chat_socket.bind(user_port)
    print(f"Live chat started for {username} on {user_port}.")

    # Function to handle incoming messages
    def handle_incoming_messages():
        while True:
            try:
                message = chat_socket.recv_json()
                print(f"\n{message['from']}: {message['message']}")
                chat_socket.send_json({"status": "received"})
            except zmq.ZMQError:
                break  # Exit when stopping the chat

    # Start a thread for incoming messages
    receiver_thread = threading.Thread(target=handle_incoming_messages, daemon=True)
    receiver_thread.start()

    # Prepare a socket for sending messages
    sender_socket = context.socket(zmq.REQ)

    # User input loop for sending messages
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            print("Exiting live chat...")
            chat_socket.close()
            sender_socket.close()
            break

        recipient_port = input("Enter recipient's port (e.g., tcp://localhost:6001): ").strip()
        try:
            sender_socket.connect(recipient_port)
            sender_socket.send_json({"from": username, "message": user_input})
            response = sender_socket.recv_json()
            if response.get("status") == "received":
                print("Message delivered successfully.")
        except zmq.ZMQError as e:
            print(f"Failed to send message: {e}")
        finally:
            sender_socket.disconnect(recipient_port)  # Disconnect after each message




from utils.friends import add_friend, remove_friend, check_user_exists

def logged_in_menu(username, user_dir):
    print(f"Debug: Entered logged_in_menu for {username}")  # Debug line
    while True:
        print(f"\nLogged in as {username}")
        print("1. Send a message")
        print("2. Check messages")
        print("3. Add a friend")
        print("4. Remove a friend")
        print("5. Check friends' status")
        print("6. List all friends")
        print("7. Start live chat")
        print("8. Logout")
        choice = input("Choose an option: ").strip()
        print(f"Debug: User selected option {choice}")  

        if choice == "1":
            recipient = input("Enter the recipient's username: ")
            message = input("Enter your message: ")
            send_message(user_dir, recipient, message, username)
        elif choice == "2":
            receive_messages(user_dir)
        elif choice == "3":
            friend = input("Enter the friend's username: ")
            add_friend(user_dir, friend)
        elif choice == "4":
            friend = input("Enter the friend's username: ")
            remove_friend(user_dir, friend)
        elif choice == "5":
            check_friends_status(user_dir, username)  # Pass current_user
        elif choice == "6":
            list_all_friends(user_dir, username)  # Pass current_user
        elif choice == "7":
            live_chat(user_dir, username)
        elif choice == "8":
            logout(username)
            break
        else:
            print("Invalid option. Please try again.")


def logout(username):
    """Mark the user as offline by updating shared file."""
    try:
        with open("server_data/online_users.json", "r+") as f:
            online_users = json.load(f)
            if username in online_users:
                del online_users[username]  # Remove the user
            f.seek(0)
            f.truncate()
            json.dump(online_users, f, indent=4)
        print(f"User '{username}' logged out successfully.")
    except Exception as e:
        print(f"Error during logout: {e}")





# Main function
def main_menu():
    """Main menu for the application."""
    while True:
        print("\nMain Menu")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def start_node():
    """Start the node and bind it to an available port."""
    context = zmq.Context()
    node_socket = context.socket(zmq.REP)
    node_port = find_available_server_port(base_port=6000, max_attempts=100)
    node_socket.bind(node_port)
    print(f"Node started and listening on {node_port}.")
    return node_socket, node_port


def bootstrap_to_network(node_port):
    print(f"Debug: Starting bootstrapping for node_port {node_port}")
    try:
        response = requests.post(f"{SERVER_ADDRESS}/register_node", json={"port": node_port}, timeout=3)
        if response.status_code == 200:
            print("Bootstrapped to the network successfully.")
        else:
            print(f"Failed to bootstrap to the network: {response.json().get('error', 'Unknown error')}")
    except requests.RequestException as e:
        print(f"Error during bootstrapping: {e}")
    print(f"Debug: Finished bootstrapping for node_port {node_port}")



if __name__ == "__main__":
    ensure_base_directory()

    # Start the node in a background thread
    node_thread = threading.Thread(target=run_node, daemon=True)
    node_thread.start()

    # Launch the CLI
    main_menu()


