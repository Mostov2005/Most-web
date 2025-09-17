import json
import sys
import os

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap, QIntValidator
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from database import DataBaseUserManager
from database import get_abs_path


# Подраздел главного окна(пополнение баланса)
class AddBalance(QMainWindow):
    back_signal = pyqtSignal()

    def __init__(self, database_user_manager, user_id):
        super().__init__()
        ui_path = get_abs_path('system_file', 'plus_balans.ui')
        loadUi(ui_path, self)

        self.move(0, 0)

        self.database_user_manager = database_user_manager
        self.user_id = user_id
        self.BALANCE_CHANGE = False

        self.poplnenie_btn.clicked.connect(self.add_summ)
        self.back_menu_btn.clicked.connect(self.switch_of_main)

        self.tec_balance = self.database_user_manager.get_balance_by_id(self.user_id)

        self.label_tec_balans.setText(f'Текущий баланс: {self.tec_balance}')
        self.label_tec_balans.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_add_summ.setValidator(self.positive_int_validator())
        self.line_add_summ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Загружаем изображение
        pixmap = QPixmap(get_abs_path('system_file', 'my_QR.png'))
        pixmap = pixmap.scaled(375, 375, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)

        # Устанавливаем изображение на QLabel
        self.label_image.setPixmap(pixmap)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
                    border-radius: 10px;
                    border: 6px solid rgb(92, 83, 220);
                """)

    def positive_int_validator(self):
        validator = QIntValidator()
        validator.setBottom(1)  # Устанавливаем минимальное значение, чтобы не было нуля и отрицательных чисел
        return validator

    def add_summ(self):
        if len(self.line_add_summ.text()) > 0:
            plus_summ = int(self.line_add_summ.text())
            self.line_add_summ.clear()
            self.tec_balance += plus_summ

            self.label_tec_balans.setText(f'Текущий баланс: {self.tec_balance}')

            self.database_user_manager.set_balance_by_id(self.user_id, self.tec_balance)

    def switch_of_main(self):
        self.back_signal.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_user_manager = DataBaseUserManager()

    add_balance_window = AddBalance(database_user_manager, 100)
    add_balance_window.show()
    sys.exit(app.exec())
