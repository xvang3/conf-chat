from hash_utils import hash_password
from file_utils import *

def register(username: str, password: str):
    username = normalize_username(username)
    data = load_data()

    if username in data:
        print(f"Registration failed: Username '{username}' already exists.")
        return

    hashed_password = hash_password(password)
    data[username] = {"password": hashed_password, "friends": [], "requests": []}
    save_data(data)
    print(f"User '{username}' registered successfully!")

# Example usage
if __name__ == "__main__":
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    register(username, password)
