import sys
import os
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi
from core import PasswordHasher
from database import DataBaseUserManager
from PyQt6.QtCore import QPropertyAnimation

from ui.registration_window import RegistrationWindow


# Вход
class WelcomeWindow(QMainWindow):
    valid_user_signal = pyqtSignal(int, str)

    def __init__(self, database_user_manager):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'system_file', 'welcome.ui')
        ui_path = os.path.abspath(ui_path)
        loadUi(ui_path, self)

        self.database_user_manager = database_user_manager
        self.registr_btn.clicked.connect(self.switch_on_registr)
        self.avt_btn.clicked.connect(self.authorization)
        self.name_edit.textChanged.connect(self.clear_error_message)
        self.paroll_edit.textChanged.connect(self.clear_error_message)

        self.name_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paroll_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def authorization(self):
        name = self.name_edit.text()
        password = self.paroll_edit.text()

        result_user = self.database_user_manager.check_valid_users(name, password)
        if result_user is None:
            self.error_label.setText("Неверное имя пользователя или пароль!")
        else:
            id_user, type_avt = result_user[0], result_user[1]
            self.valid_user_signal.emit(int(id_user), str(type_avt))  # Сигнал с типом
            return

        self.error_label.setText("Неверное имя пользователя или пароль!")

    def clear_error_message(self):
        self.error_label.clear()

    def switch_on_registr(self):
        self.name_edit.clear()
        self.paroll_edit.clear()
        self.error_label.clear()
        self.registration_window = RegistrationWindow(self.database_user_manager)
        self.registration_window.back_signal.connect(self.show_window)
        # Анимация появления нового окна
        self.fade_in(self.registration_window)
        self.registration_window.show()

        # Анимация скрытия текущего окна
        self.fade_out(self)

    def show_window(self):
        # Анимация появления welcome
        self.fade_in(self)
        self.show()

        # Анимация скрытия регистрации
        self.fade_out(self.registration_window)
        self.registration_window.close()

    def fade_in(self, widget):
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(400)  # 400 мс
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.start()
        widget._anim = anim  # сохраняем, иначе сборщик мусора убьёт анимацию

    def fade_out(self, widget):
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(400)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.start()
        widget._anim = anim


if __name__ == "__main__":
    database_user_manager = DataBaseUserManager()

    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow(database_user_manager)
    welcome_window.show()
    sys.exit(app.exec())  # Запуск приложения
