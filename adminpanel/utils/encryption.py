from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

def _get_cipher():
    key = settings.ENCRYPTION_KEY.encode()
    return Fernet(key)

def encrypt_id(value: int) -> str:
    cipher = _get_cipher()
    return cipher.encrypt(str(value).encode()).decode()

def decrypt_id(token: str) -> int:
    cipher = _get_cipher()
    try:
        return int(cipher.decrypt(token.encode()).decode())
    except InvalidToken:
        raise ValueError("Invalid or tampered token")


def encrypt_password(password: str) -> str:
    cipher = _get_cipher()
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password: str) -> str:
    cipher = _get_cipher()
    return cipher.decrypt(encrypted_password.encode()).decode()