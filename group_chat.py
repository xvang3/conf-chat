from utils.storage import load_local_data, save_local_data

def create_group_chat():
    username = input("Your username: ").strip()
    group_name = input("Group name: ").strip()

    data = load_local_data()
    data[username]["groups"].append(group_name)
    save_local_data(data)
    print(f"Group '{group_name}' created.")

def leave_group_chat():
    username = input("Your username: ").strip()
    group_name = input("Group name: ").strip()

    data = load_local_data()
    if group_name not in data[username]["groups"]:
        print(f"You are not part of the group '{group_name}'.")
        return
    data[username]["groups"].remove(group_name)
    save_local_data(data)
    print(f"You left the group '{group_name}'.")

def destroy_group_chat():
    print("Feature not implemented yet.")
