import asyncio
from kademlia_node import KademliaNode
from hash_utils import *

# Initialize the Kademlia node with a dynamic port
kademlia_node = KademliaNode(port=8468)

async def register_user():
    """Register a new user."""
    print("\n--- User Registration ---")
    username = input("Enter a username: ").strip()
    password = input("Enter a password: ").strip()
    confirm_password = input("Confirm your password: ").strip()

    if password != confirm_password:
        print("Error: Passwords do not match!")
        return

    hashed_password = hash_password(password)
    user_data = {
        "password": hashed_password,
        "friends": [],
        "requests": [],
        "messages": []
    }

    key = f"user:{username}"
    print(f"Storing user: {user_data}")
    await kademlia_node.store(key, user_data)
    print(f"User '{username}' successfully registered!")

async def login_user():
    """Log in an existing user."""
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    key = f"user:{username}"
    print(f"Retrieving key: {key}")
    user_data = await kademlia_node.retrieve(key)

    if not user_data:
        print("Error: User does not exist.")
        return None

    if verify_password(password, user_data["password"]):
        print(f"Welcome, {username}!")
        return username
    else:
        print("Error: Incorrect password.")
        return None

async def main_menu():
    """Display the main menu."""
    while True:
        print("\nMain Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            await register_user()
        elif choice == "2":
            logged_in_user = await login_user()
            if logged_in_user:
                print(f"User '{logged_in_user}' logged in!")
        elif choice == "3":
            print("Goodbye!")
            await kademlia_node.stop()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(kademlia_node.start())
    asyncio.run(main_menu())
