from utils.storage import load_local_data, save_local_data

def register():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    data = load_local_data()
    if username in data:
        print("User already exists.")
        return
    data[username] = {"password": password, "friends": [], "messages": [], "groups": []}
    save_local_data(data)
    print(f"User '{username}' registered successfully.")

def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    data = load_local_data()
    if username in data and data[username]["password"] == password:
        print(f"Welcome back, {username}!")
    else:
        print("Invalid username or password.")

def logout():
    print("Logged out successfully.")
