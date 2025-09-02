import hashlib


# Хешер паролей(для регистрации)
class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        hash_object = hashlib.sha256()
        hash_object.update(password.encode())
        hashed_password = hash_object.hexdigest()

        return hashed_password
