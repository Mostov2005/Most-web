import re


def validate_login(text):
    if len(text) < 5:
        return 'Логин должен состоять не менее чем из 5 символов'
    elif re.search(r'[^a-zA-Z0-9]', text):
        return 'В логине могут использоваться только буквы латинского алфавита и цифры'
    return None


def validate_phone(text):
    if len(text) < 18:
        return 'Неверно введен номер телефона'
    return None


def validate_password(text):
    if len(text) < 8:
        return 'Пароль должен состоять не менее чем из 8 символов'

    elif not re.search('[a-z]', text):
        return 'Пароль должен содержать как минимум одну строчную букву латинского алфавита'

    elif not re.search('[A-Z]', text):
        return 'Пароль должен содержать как минимум одну прописную букву латинского алфавита'

    elif not re.search('[0-9]', text):
        return 'Пароль должен содержать хотя бы одну цифру'

    elif not re.search('[!@#$%^&*(),.?":{}|<>_-]', text):
        return 'Пароль должен содержать хотя бы один специальный символ'
    return None


