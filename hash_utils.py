import hashlib

def hash_password(password):
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """
    Verify if the given password matches the hashed password.
    
    :param password: The plaintext password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if they match, False otherwise.
    """
    return hash_password(password) == hashed_password
