import json
import os

LOCAL_FILE = "peer_data.json"

def load_local_data():
    if not os.path.exists(LOCAL_FILE):
        with open(LOCAL_FILE, "w") as f:
            json.dump({}, f)
    with open(LOCAL_FILE, "r") as f:
        return json.load(f)

def save_local_data(data):
    with open(LOCAL_FILE, "w") as f:
        json.dump(data, f, indent=4)
