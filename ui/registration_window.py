import sys

from PyQt6.QtCore import Qt, QRegularExpression, pyqtSignal
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi

import qt_env  # noqa: F401
from database import DataBaseUserManager, get_abs_path
from ui.info_window import InfoWindow
from utils.validators import validate_login, validate_phone, validate_password


class RegistrationWindow(QMainWindow):
    """Окно регистрации нового пользователя"""
    back_signal = pyqtSignal()

    def __init__(self, database_user_manager: DataBaseUserManager):
        super().__init__()
        ui_path = get_abs_path('system_file', 'registration.ui')
        loadUi(ui_path, self)

        self.database_user_manager = database_user_manager

        self.back_btn.clicked.connect(self.switch_on_welcome)
        self.registr_btn.clicked.connect(self.validate_registration)

        # Выравнивание полей ввода
        for edit in [self.login_edit, self.email_edit, self.phone_edit, self.paroll_edit, self.paroll_return_edit]:
            edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Подключение слотов для проверки ввода
        self.login_edit.textChanged.connect(self.login_valid)
        self.email_edit.textChanged.connect(self.valid_email)
        self.phone_edit.textChanged.connect(self.valid_phone)
        self.paroll_edit.textChanged.connect(self.valid_password)
        self.paroll_return_edit.textChanged.connect(self.valid_return_password)

        # Маска и placeholder для телефона
        self.phone_edit.setPlaceholderText("+7 (___) ___-__-__")
        self.phone_edit.setInputMask("+7 (999) 999-99-99")
        self.phone_edit.mousePressEvent = lambda event: None

        # Валидатор email
        email_validator = QRegularExpressionValidator(
            QRegularExpression(r'^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$'), self.email_edit)
        self.email_edit.setValidator(email_validator)

        self.clear_fields()

    def validate_registration(self):
        """Проверяет все поля и регистрирует пользователя"""
        self.error_registration_label.clear()

        login = self.login_edit.text()
        email = self.email_edit.text()
        phone = self.phone_edit.text()
        password = self.paroll_edit.text()
        return_password = self.paroll_return_edit.text()

        # Проверка валидности всех полей
        if not (self.login_valid(login) and
                self.valid_email() and
                self.valid_phone(phone) and
                self.valid_password(password) and
                self.valid_return_password(return_password)):
            self.error_registration_label.setText("Заполните все поля!")
            return

        # Проверка уникальности логина, email и телефона
        if self.database_user_manager.check_user_availability(login):
            self.error_login_label.setText('Пользователь с таким логином уже существует!')
            return

        if self.database_user_manager.check_email_availability(email):
            self.error_email_label.setText('Пользователь с таким email уже существует')
            return

        if self.database_user_manager.check_phone_availability(phone):
            self.error_phone_label.setText('Пользователь с таким номером телефона уже существует')
            return

        # Добавление нового пользователя
        try:
            self.database_user_manager.add_new_user(login, email, phone, password)
            self.info_window = InfoWindow("Успех", "Регистрация прошла успешно!")
            self.info_window.show()
        except Exception as e:
            print(str(e))

    def login_valid(self, text: str) -> bool:
        self.error_login_label.clear()
        result = validate_login(text)
        if result:
            self.error_login_label.setText(result)
            return False
        return True

    def valid_email(self) -> bool:
        self.error_email_label.clear()
        if not self.email_edit.hasAcceptableInput():
            self.error_email_label.setText("Введен некорректный email")
            return False
        return True

    def valid_phone(self, text: str) -> bool:
        self.error_phone_label.clear()
        result = validate_phone(text)
        if result:
            self.error_phone_label.setText(result)
            return False
        return True

    def valid_password(self, text: str) -> bool:
        self.error_parol_label.clear()
        result = validate_password(text)
        if result:
            self.error_parol_label.setText(result)
            return False
        return True

    def valid_return_password(self, text: str) -> bool:
        self.error_return_paroll_label.clear()
        if text != self.paroll_edit.text():
            self.error_return_paroll_label.setText('Пароли не совпадают')
            return False
        return True

    def clear_fields(self) -> None:
        """Очищает все поля ввода и ошибки"""
        for edit in [self.login_edit, self.email_edit, self.phone_edit, self.paroll_edit, self.paroll_return_edit]:
            edit.clear()
        for label in [self.error_login_label, self.error_email_label, self.error_parol_label,
                      self.error_phone_label, self.error_return_paroll_label, self.error_registration_label]:
            label.clear()

    def switch_on_welcome(self) -> None:
        self.back_signal.emit()


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    database_user_manager = DataBaseUserManager()
    registration_window = RegistrationWindow(database_user_manager)
    registration_window.show()
    sys.exit(app.exec())
