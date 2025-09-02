import json
import sys
import re
import os
import shutil

from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QRect, QEasingCurve, Qt, QRegularExpression
from PyQt6.QtGui import QPixmap, QIntValidator, QFont, QRegularExpressionValidator
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QRadioButton, QButtonGroup, QComboBox, QFileDialog
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QMainWindow, QMessageBox, QLineEdit

from core import PasswordHasher


# Подраздел главного окна(пополнение баланса)
class Poplnenie_balansa(QMainWindow):
    balance_updated = pyqtSignal(str)

    def __init__(self, name):
        super().__init__()
        loadUi("system_file\\plus_balans.ui", self)
        self.move(0, 0)

        self.poplnenie_btn.clicked.connect(self.add_summ)
        self.back_menu_btn.clicked.connect(self.swith_of_main)

        self.name_polzovatel = name
        self.tec_balans = users[self.name_polzovatel][5]
        self.label_tec_balans.setText(f'Текущий баланс: {self.tec_balans}')
        self.label_tec_balans.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_add_summ.setValidator(self.positive_int_validator())
        self.line_add_summ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Загружаем изображение
        pixmap = QPixmap("system_file\\my_QR.png")
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
            self.tec_balans += plus_summ

            self.label_tec_balans.setText(f'Текущий баланс: {self.tec_balans}')

            users[self.name_polzovatel][5] = self.tec_balans
            with open('system_file\\users.csv', 'w') as file:
                json.dump(users, file, ensure_ascii=False, indent=2)

            # Emit signal
            self.balance_updated.emit(self.name_polzovatel)

    def swith_of_main(self):
        self.hide()
        main_window.show()
