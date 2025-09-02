import sys
import json
import re
import os

from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi

from utils.validators import (
    validate_login, validate_email, validate_phone,
    validate_password, validate_password_repeat
)
from database import DataBaseManager
from core import PasswordHasher


# Регистрация
class RegistrationWindow(QMainWindow):
    def __init__(self, database_manager):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'system_file', 'registration.ui')
        ui_path = os.path.abspath(ui_path)
        loadUi(ui_path, self)

        self.database_manager = database_manager

        self.back_btn.clicked.connect(self.switch_on_welcome)
        # Установка выравнивания для полей ввода
        self.login_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.email_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phone_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paroll_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paroll_return_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Подключение слотов к событиям изменения текста
        self.login_edit.textChanged.connect(self.login_valid)
        self.email_edit.textChanged.connect(self.valid_email)
        self.paroll_edit.textChanged.connect(self.valid_passsword)
        self.paroll_return_edit.textChanged.connect(self.valid_return_password)

        self.flag_login = False
        self.flag_email = False
        self.flag_phone = False
        self.flag_paroll = False
        self.flag_return_paroll = False

        # Подключение слота к кнопке регистрации
        self.registr_btn.clicked.connect(self.valid_registration)

        # Установка маски и игнорирование события для поля ввода номера телефона
        self.phone_edit.setPlaceholderText("+7 (___) ___-__-__")
        self.phone_edit.setInputMask("+7 (999) 999-99-99")
        self.phone_edit.mousePressEvent = self.ignore_event
        self.phone_edit.textChanged.connect(self.valid_phone)

        # Установка валидатора для поля ввода email
        email_validator = QRegularExpressionValidator(
            QRegularExpression(r'^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$'), self.email_edit)
        self.email_edit.setValidator(email_validator)

    def login_valid(self, text):
        self.flag_login = False
        self.error_login_label.clear()  # Очищаем сообщение об ошибке
        self.error_registration_label.clear()

        result = validate_login(text)
        if result:
            self.error_login_label.setText(result)
            return

        if self.database_manager.check_user_availability(text):
            self.error_login_label.setText('Пользователь с таким логином уже существует')

        else:
            self.flag_login = True


    def valid_email(self):
        print('ds')


    def valid_passsword(self):
        print('ds')


    def valid_return_password(self):
        print('ds')


    def valid_phone(self):
        print('ds')


    def valid_registration(self):
        print('ds')


    def clear_fields(self):
        self.login_edit.clear()
        self.email_edit.clear()
        self.phone_edit.clear()
        self.paroll_edit.clear()
        self.paroll_return_edit.clear()

        self.error_login_label.clear()
        self.error_email_label.clear()
        self.error_parol_label.clear()
        self.error_phone_label.clear()
        self.error_return_paroll_label.clear()
        self.error_registration_label.clear()


    def switch_on_welcome(self):
        self.clear_fields()
        self.close()


    def ignore_event(self, event):
        pass


    def validate_registration(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_manager = DataBaseManager()
    registration_window = RegistrationWindow(database_manager)
    registration_window.show()
    sys.exit(app.exec())  # Запуск приложения
