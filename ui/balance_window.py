import sys
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QIntValidator
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from database import DataBaseUserManager, get_abs_path


# Подраздел главного окна (пополнение баланса)
class AddBalance(QMainWindow):
    """Окно пополнения баланса пользователя"""
    back_signal = pyqtSignal()

    def __init__(self, database_user_manager: DataBaseUserManager, user_id: int) -> None:
        super().__init__()
        ui_path: str = get_abs_path('system_file', 'plus_balans.ui')
        loadUi(ui_path, self)

        self.move(0, 0)

        self.database_user_manager: DataBaseUserManager = database_user_manager
        self.user_id: int = user_id
        self.tec_balance: int = self.database_user_manager.get_balance_by_id(self.user_id)
        self.BALANCE_CHANGE: bool = False

        self.poplnenie_btn.clicked.connect(self.add_summ)
        self.back_menu_btn.clicked.connect(self.switch_of_main)

        self.label_tec_balans.setText(f'Текущий баланс: {self.tec_balance}')
        self.label_tec_balans.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_add_summ.setValidator(self.positive_int_validator())
        self.line_add_summ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Загружаем изображение
        pixmap: QPixmap = QPixmap(get_abs_path('system_file', 'my_QR.png'))
        pixmap = pixmap.scaled(375, 375, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)
        self.label_image.setPixmap(pixmap)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
                    border-radius: 10px;
                    border: 6px solid rgb(92, 83, 220);
                """)

    def positive_int_validator(self) -> QIntValidator:
        """Валидатор для положительных целых чисел"""
        validator = QIntValidator()
        validator.setBottom(1)
        return validator

    def add_summ(self) -> None:
        """Добавление суммы к текущему балансу пользователя"""
        if len(self.line_add_summ.text()) > 0:
            plus_summ: int = int(self.line_add_summ.text())
            self.line_add_summ.clear()
            self.tec_balance += plus_summ

            self.label_tec_balans.setText(f'Текущий баланс: {self.tec_balance}')
            self.database_user_manager.set_balance_by_id(self.user_id, self.tec_balance)

    def switch_of_main(self) -> None:
        """Возврат в главное меню"""
        self.back_signal.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_user_manager: DataBaseUserManager = DataBaseUserManager()

    add_balance_window: AddBalance = AddBalance(database_user_manager, 100)
    add_balance_window.show()
    sys.exit(app.exec())
