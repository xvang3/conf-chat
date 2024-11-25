import os
import json
from flask import Flask, request, jsonify

# Flask app setup
app = Flask(__name__)

# Server data directories and files
SERVER_BASE_DIR = os.path.join(os.getcwd(), "server_data")
USERS_FILE = os.path.join(SERVER_BASE_DIR, "users.json")
ONLINE_USERS_FILE = os.path.join(SERVER_BASE_DIR, "online_users.json")


# Ensure server data directories and files exist
def ensure_server_files():
    """Ensure all necessary server files are properly initialized."""
    if not os.path.exists(SERVER_BASE_DIR):
        os.makedirs(SERVER_BASE_DIR)

    # Initialize users.json
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)
        print("Initialized users.json file.")

    # Initialize online_users.json
    if not os.path.exists(ONLINE_USERS_FILE):
        with open(ONLINE_USERS_FILE, "w") as f:
            json.dump({}, f)  # Use dictionary for better mapping
        print("Initialized online_users.json file.")


ensure_server_files()


# Utility functions
def get_all_users():
    """Retrieve the list of all registered users."""
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
            if not isinstance(users, list):
                raise ValueError
        return users
    except (json.JSONDecodeError, ValueError):
        print("Corrupted users.json file detected. Reinitializing...")
        with open(USERS_FILE, "w") as f:
            json.dump([], f)
        return []


def add_user(username):
    """Add a new user to users.json."""
    users = get_all_users()
    if username not in users:
        users.append(username)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
        print(f"User '{username}' added to users.json.")
    else:
        print(f"User '{username}' already exists in users.json.")


def get_online_users():
    """Retrieve the list of currently online users."""
    try:
        with open(ONLINE_USERS_FILE, "r") as f:
            online_users = json.load(f)
            if not isinstance(online_users, dict):
                raise ValueError
        return online_users
    except (json.JSONDecodeError, ValueError):
        print("Corrupted online_users.json file detected. Reinitializing...")
        with open(ONLINE_USERS_FILE, "w") as f:
            json.dump({}, f)
        return {}


def update_online_users(username, action):
    """Update the online_users.json file."""
    online_users = get_online_users()
    if action == "login" and username not in online_users:
        online_users.append(username)
    elif action == "logout" and username in online_users:
        online_users.remove(username)
    with open(ONLINE_USERS_FILE, "w") as f:
        json.dump(online_users, f, indent=4)
    print(f"User '{username}' marked as {action}.")


# Flask Endpoints
@app.route("/user_status", methods=["POST"])
def user_status():
    """Update user status (online/offline)."""
    data = request.json
    username = data.get("username")
    action = data.get("action")  # "login" or "logout"

    if not username or action not in ["login", "logout"]:
        return jsonify({"error": "Invalid request"}), 400

    update_online_users(username, action)
    return jsonify({"message": f"User '{username}' marked as {action}."}), 200



@app.route("/add_user", methods=["POST"])
def add_user_endpoint():
    """Register a new user."""
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    add_user(username)
    return jsonify({"message": f"User '{username}' added successfully."}), 200


@app.route("/get_online_users", methods=["GET"])
def get_online_users_endpoint():
    """Retrieve the list of online users."""
    online_users = get_online_users()
    return jsonify({"online_users": online_users}), 200


@app.route("/get_all_users", methods=["GET"])
def get_all_users_endpoint():
    """Retrieve the list of all registered users."""
    users = get_all_users()
    return jsonify({"users": users}), 200


# Server Startup
if __name__ == "__main__":
    print("Starting server...")
    app.run(host="0.0.0.0", port=5555)
