import os
import sys

from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSignal

from core import PasswordHasher
from database import DataBaseUserManager
from utils.validators import validate_login, validate_phone, validate_password
from ui.info_window import InfoWindow


# Регистрация
class RegistrationWindow(QMainWindow):
    back_signal = pyqtSignal()

    def __init__(self, database_user_manager):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'system_file', 'registration.ui')
        ui_path = os.path.abspath(ui_path)
        loadUi(ui_path, self)

        self.database_user_manager = database_user_manager

        self.back_btn.clicked.connect(self.switch_on_welcome)
        self.registr_btn.clicked.connect(self.validate_registration)

        # Установка выравнивания для полей ввода
        self.login_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.email_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phone_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paroll_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paroll_return_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Подключение слотов к событиям изменения текста
        self.login_edit.textChanged.connect(self.login_valid)
        self.email_edit.textChanged.connect(self.valid_email)
        self.phone_edit.textChanged.connect(self.valid_phone)
        self.paroll_edit.textChanged.connect(self.valid_password)
        self.paroll_return_edit.textChanged.connect(self.valid_return_password)

        # Установка маски и игнорирование события для поля ввода номера телефона
        self.phone_edit.setPlaceholderText("+7 (___) ___-__-__")
        self.phone_edit.setInputMask("+7 (999) 999-99-99")
        self.phone_edit.mousePressEvent = lambda event: None

        # Установка валидатора для поля ввода email
        email_validator = QRegularExpressionValidator(
            QRegularExpression(r'^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$'), self.email_edit)
        self.email_edit.setValidator(email_validator)

        self.clear_fields()

    def validate_registration(self):
        self.error_registration_label.clear()

        login = self.login_edit.text()
        email = self.email_edit.text()
        phone = self.phone_edit.text()
        password = self.paroll_edit.text()
        return_password = self.paroll_return_edit.text()

        if not (self.login_valid(login) and
                self.valid_email() and
                self.valid_phone(phone) and
                self.valid_password(password) and
                self.valid_return_password(return_password)
        ):
            self.error_registration_label.setText("Заполните все поля!")
            return

        if self.database_user_manager.check_user_availability(login):
            self.error_login_label.setText('Пользователь с таким логином уже существует!')
            return

        if self.database_user_manager.check_email_availability(email):
            self.error_email_label.setText('Пользователь с таким email уже существует')
            return

        if self.database_user_manager.check_phone_availability(phone):
            self.error_phone_label.setText('Пользователь с таким номером телефона уже существует')
            return

        try:
            self.database_user_manager.add_new_user(login, email, phone, password)
            self.info_window = InfoWindow("Успех", "Регистрация прошла успешно!")
            self.info_window.show()
        except Exception as e:
            print((str(e)))
            return

    def login_valid(self, text):
        self.error_login_label.clear()  # Очищаем сообщение об ошибке
        result = validate_login(text)
        if result:
            self.error_login_label.setText(result)
            return False
        return True

    def valid_email(self):
        self.error_email_label.clear()  # Очищаем сообщение об ошибке
        if not self.email_edit.hasAcceptableInput():
            self.error_email_label.setText("Введен некорректный email")
            return False
        return True

    def valid_phone(self, text):
        self.error_phone_label.clear()  # Очищаем сообщение об ошибке
        result = validate_phone(text)
        if result:
            self.error_phone_label.setText(result)
            return False
        return True

    def valid_password(self, text):
        self.error_parol_label.clear()
        result = validate_password(text)
        if result:
            self.error_parol_label.setText(result)
            return False
        return True

    def valid_return_password(self, text):
        self.error_return_paroll_label.clear()
        if text != self.paroll_edit.text():
            self.error_return_paroll_label.setText('Пароли не совпадают')
            return False
        return True

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
        self.back_signal.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_user_manager = DataBaseUserManager()
    registration_window = RegistrationWindow(database_user_manager)
    registration_window.show()
    sys.exit(app.exec())
