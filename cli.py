from user_status import *
from file_utils import *
from hash_utils import *
from check_online_friends import *

# Global variable to track logged-in user
logged_in_user = None

def main_menu():
    """Display the main menu for the logged-in user."""
    while True:
        print("\nMenu:")
        print("1. Check online friends")
        print("2. Logout")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            if logged_in_user:
                check_online_friends(logged_in_user)
            else:
                print("You must log in first.")
        elif choice == "2":
            if logged_in_user:
                logout_user(logged_in_user)
                break
            else:
                print("You are not logged in.")
        elif choice == "3":
            print("Goodbye!")
            exit(0)
        else:
            print("Invalid choice. Please try again.")

def login_menu():
    """Display the login menu."""
    global logged_in_user

    while not logged_in_user:
        print("\nLogin Menu:")
        print("1. Login")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            # Normalize the username
            username = normalize_username(username)

            # Validate user credentials
            data = load_data()
            if username not in data:
                print(f"Login failed: User '{username}' does not exist.")
                continue

            if data[username]["password"] != hash_password(password):
                print("Login failed: Incorrect password.")
                continue

            # Successful login
            login_user(username)
            logged_in_user = username
            print(f"Welcome, {logged_in_user}!")
            main_menu()  # Transition to main menu
        elif choice == "2":
            print("Goodbye!")
            exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    login_menu()
