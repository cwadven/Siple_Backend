from cryptography.fernet import Fernet
from django.conf import settings


fernet = Fernet(settings.SECRET_KEY)


def encrypt_integer(integer: int) -> str:
    integer_bytes = str(integer).encode()
    encrypted = fernet.encrypt(integer_bytes)
    return str(encrypted)


def decrypt_integer(encrypted: str) -> int:
    decrypted_bytes = fernet.decrypt(encrypted)
    decrypted_integer = int(decrypted_bytes.decode())
    return decrypted_integer
