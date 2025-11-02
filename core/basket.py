# import json
# import sys
# import re
# import os
# import shutil
#
# from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QRect, QEasingCurve, Qt, QRegularExpression
# from PyQt6.QtGui import QPixmap, QIntValidator, QFont, QRegularExpressionValidator
# from PyQt6.uic import loadUi
# from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QRadioButton, QButtonGroup, QComboBox, QFileDialog
# from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QMainWindow, QMessageBox, QLineEdit
#
# from core import PasswordHasher
#
#
# # Заполнение таблицы(Подраздел главного окна)
# class ProductWidget(QWidget):
#     def __init__(self, name, price, image_path, parent=None):
#         super(ProductWidget, self).__init__(parent)
#         layout = QVBoxLayout()
#
#         font = QFont()
#         font.setPointSize(14)
#         font.setFamily("Arial")
#
#         self.name_label = QLabel(name)
#         self.name_label.setFont(font)
#         self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.name_label)
#
#         self.image_label = QLabel()
#         pixmap = QPixmap(image_path)
#         pixmap = pixmap.scaled(300, 400, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)
#
#         self.image_label.setStyleSheet("""
#             border-radius: 10px;
#             border: 6px solid rgb(92, 83, 220);
#         """)
#         self.image_label.setPixmap(pixmap)
#
#         layout.addWidget(self.image_label)
#
#         self.price_label = QLabel(f"{price} ₽")
#         self.price_label.setFont(font)
#         self.price_label.setStyleSheet("color: rgb(167, 58, 253); font-weight: bold;")
#         self.price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.price_label)
#
#         self.buy_button = QPushButton("Добавить в корзину")
#         self.buy_button.clicked.connect(lambda: self.add_tovar_in_basket(name, price))
#         self.buy_button.setFont(font)
#         self.buy_button.setStyleSheet("""
#             QPushButton {
#                 border-radius: 10px;
#                 color: white;
#                 background-color: rgb(92, 83, 220);
#             }
#             QPushButton:hover {
#                 background-color: rgb(73, 17, 127);
#             }
#             QPushButton:pressed {
#                 background-color: rgb(50, 0, 100);
#             }
#         """)
#         self.buy_button.setFixedSize(280, 30)
#         layout.addWidget(self.buy_button)
#
#         self.setLayout(layout)
#
#     def add_tovar_in_basket(self, name_tovar, price):
#         global summ_basket
#         basket.append(name_tovar)
#         summ_basket += price
#         main_window.update_basket_label()
