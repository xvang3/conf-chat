from utils.storage import load_local_data

def list_all_users():
    """List all registered users."""
    data = load_local_data()
    if not data:
        print("No users found.")
        return
    print("Registered Users:")
    for username in data:
        print(f"- {username}")

def show_user_details(username):
    """Show details for a specific user."""
    data = load_local_data()
    if username not in data:
        print(f"User '{username}' does not exist.")
        return
    user_details = data[username]
    print(f"Details for user '{username}':")
    print(f"  Password: {user_details['password']}")
    print(f"  Friends: {', '.join(user_details['friends']) if user_details['friends'] else 'None'}")
    print(f"  Groups: {', '.join(user_details['groups']) if user_details['groups'] else 'None'}")
    print(f"  Messages: {len(user_details['messages'])} messages")

def count_users():
    """Count the total number of registered users."""
    data = load_local_data()
    print(f"Total registered users: {len(data)}")

def count_online_users():
    """Count the number of users currently online."""
    # Placeholder: Replace this with actual online status logic if implemented
    print("Feature not implemented yet: Assuming no online tracking exists.")

def run_master_command():
    """CLI for master commands."""
    while True:
        print("\n=== Master Commands ===")
        print("1. List all users")
        print("2. Show user details")
        print("3. Count total users")
        print("4. Count online users")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_all_users()
        elif choice == "2":
            username = input("Enter username to view details: ").strip()
            show_user_details(username)
        elif choice == "3":
            count_users()
        elif choice == "4":
            count_online_users()
        elif choice == "5":
            print("Exiting master commands.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    run_master_command()
