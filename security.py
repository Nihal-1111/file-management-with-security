from cryptography.fernet import Fernet
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(BASE_DIR, "secret.key")

# ---------------- Key Management ----------------
def generate_key():
    """Generate a new secret.key file"""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    """Load the key (generate if missing)"""
    if not os.path.exists(KEY_FILE):
        generate_key()
    return open(KEY_FILE, "rb").read()

# ---------------- Encryption ----------------
def encrypt_file(file_path):
    """Encrypt a file in place"""
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        original_data = file.read()

    encrypted_data = fernet.encrypt(original_data)

    with open(file_path, "wb") as file:
        file.write(encrypted_data)

# ---------------- Decryption ----------------
def decrypt_file(file_path):
    """Decrypt a file in place"""
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(file_path, "wb") as file:
        file.write(decrypted_data)
SEC_FILE = os.path.join                     