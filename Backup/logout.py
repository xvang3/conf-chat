from user_status import logout_user
from file_utils import normalize_username

def logout(username: str):
    username = normalize_username(username)
    logout_user(username)
