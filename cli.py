from user_status import login_user, logout_user
from friend_management import check_online_friends
from file_utils import normalize_username

def main():
    while True:
        print("\nMenu:")
        print("1. Log in")
        print("2. Log out")
        print("3. Check online friends")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            login_user(normalize_username(username))
        elif choice == "2":
            username = input("Enter your username: ")
            logout_user(normalize_username(username))
        elif choice == "3":
            username = input("Enter your username: ")
            check_online_friends(normalize_username(username))
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
