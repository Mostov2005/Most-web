import re
from typing import Optional


def validate_login(text: str) -> Optional[str]:
    """Проверяет корректность логина."""
    if len(text) < 5:
        return "Логин должен состоять не менее чем из 5 символов"
    if re.search(r"[^a-zA-Z0-9]", text):
        return "В логине могут использоваться только буквы латинского алфавита и цифры"
    return None


def validate_phone(text: str) -> Optional[str]:
    """Проверяет корректность номера телефона."""
    if len(text) < 18:
        return "Неверно введен номер телефона"
    return None


def validate_password(text: str) -> Optional[str]:
    """Проверяет корректность пароля по сложности."""
    if len(text) < 8:
        return "Пароль должен состоять не менее чем из 8 символов"
    if not re.search(r"[a-z]", text):
        return "Пароль должен содержать как минимум одну строчную букву латинского алфавита"
    if not re.search(r"[A-Z]", text):
        return "Пароль должен содержать как минимум одну прописную букву латинского алфавита"
    if not re.search(r"[0-9]", text):
        return "Пароль должен содержать хотя бы одну цифру"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_-]", text):
        return "Пароль должен содержать хотя бы один специальный символ"
    return None
