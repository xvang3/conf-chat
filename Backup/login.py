from hash_utils import hash_password
from file_utils import *
from user_status import *

def login(username: str, password: str):
    username = normalize_username(username)
    data = load_data()

    if username not in data:
        print("Login failed: User not found.")
        return

    if data[username]["password"] == hash_password(password):
        print(f"Login successful! Welcome, {username}.")
        login_user(username)
    else:
        print("Login failed: Incorrect password.")

# Example usage
if __name__ == "__main__":
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    login(username, password)
