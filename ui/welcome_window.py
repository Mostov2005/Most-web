import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi

from database import DataBaseUserManager, get_abs_path
from ui.registration_window import RegistrationWindow


class WelcomeWindow(QMainWindow):
    """Главное окно входа пользователя"""
    valid_user_signal = pyqtSignal(int, str)

    def __init__(self, database_user_manager: DataBaseUserManager):
        super().__init__()
        ui_path = get_abs_path('system_file', 'welcome.ui')
        loadUi(ui_path, self)

        self.database_user_manager = database_user_manager

        # Кнопки
        self.registr_btn.clicked.connect(self.switch_on_registr)
        self.avt_btn.clicked.connect(self.authorization)

        # Поля ввода
        self.name_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paroll_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_edit.textChanged.connect(self.clear_error_message)
        self.paroll_edit.textChanged.connect(self.clear_error_message)

    def authorization(self):
        """Проверяет логин и пароль"""
        name = self.name_edit.text()
        password = self.paroll_edit.text()

        result_user = self.database_user_manager.check_valid_users(name, password)
        if result_user is None:
            self.error_label.setText("Неверное имя пользователя или пароль!")
            return

        user_id, type_avt = result_user
        self.valid_user_signal.emit(int(user_id), str(type_avt))

    def clear_error_message(self):
        """Очищает сообщение об ошибке при вводе"""
        self.error_label.clear()

    def switch_on_registr(self):
        """Переход на окно регистрации с анимацией"""
        self.name_edit.clear()
        self.paroll_edit.clear()
        self.error_label.clear()

        self.registration_window = RegistrationWindow(self.database_user_manager)
        self.registration_window.back_signal.connect(self.show_window)

        self.fade_in(self.registration_window)
        self.registration_window.show()
        self.fade_out(self)

    def show_window(self):
        """Возврат к окну входа с анимацией и закрытие окна регистрации"""
        self.fade_in(self)
        self.show()
        self.fade_out(self.registration_window)
        self.registration_window.close()

    def fade_in(self, widget):
        """Анимация появления окна"""
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(400)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.start()
        widget._anim = anim  # Сохраняем ссылку, чтобы сборщик мусора не удалил анимацию

    def fade_out(self, widget):
        """Анимация скрытия окна"""
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(400)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.start()
        widget._anim = anim


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_user_manager = DataBaseUserManager()

    welcome_window = WelcomeWindow(database_user_manager)
    welcome_window.show()
    sys.exit(app.exec())
