import hashlib


# Хешер паролей (для регистрации)
class PasswordHasher:
    """Класс для хеширования паролей"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Возврат SHA-256 хеша пароля"""
        hash_object: hashlib._Hash = hashlib.sha256()
        hash_object.update(password.encode('utf-8'))
        hashed_password: str = hash_object.hexdigest()
        return hashed_password
