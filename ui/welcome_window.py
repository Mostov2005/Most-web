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
from database import DataBaseManager


# Вход
class WelcomeWindow(QMainWindow):
    valid_user_signal = pyqtSignal(int, str)

    def __init__(self, data_base_manager):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'system_file', 'welcome.ui')
        ui_path = os.path.abspath(ui_path)
        loadUi(ui_path, self)

        self.data_base_manager = data_base_manager
        # self.registr_btn.clicked.connect(self.switch_on_registr)
        self.avt_btn.clicked.connect(self.authorization)
        self.name_edit.textChanged.connect(self.clear_error_message)
        self.paroll_edit.textChanged.connect(self.clear_error_message)

        self.name_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paroll_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def authorization(self):
        name = self.name_edit.text()
        password = self.paroll_edit.text()

        result_user = self.data_base_manager.check_valid_users(name, password)
        if result_user is None:
            self.error_label.setText("Неверное имя пользователя или пароль!")
        else:
            id_user, type_avt = result_user[0], result_user[1]
            print(int(id_user), str(type_avt))
            self.valid_user_signal.emit(int(id_user), str(type_avt))  # Сигнал с типом авторизации

        self.error_label.setText("Неверное имя пользователя или пароль!")

    def clear_error_message(self):
        self.error_label.clear()

    # def switch_on_registr(self):
    #     self.name_edit.clear()
    #     self.paroll_edit.clear()
    #     self.error_label.clear()
    #     registr_window.show()
    #     self.close()
    #


if __name__ == "__main__":
    databasemanager = DataBaseManager()

    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow(databasemanager)
    welcome_window.show()
    sys.exit(app.exec())  # Запуск приложения
