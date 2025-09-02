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


# Добавление товаров(Подраздел для работников)
class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(400, 300)

        self.name_edit = QLineEdit()
        self.price_edit = QLineEdit()
        self.image_label = QLabel("Изображение не выбрано")
        self.browse_button = QPushButton("Выбрать изображение")
        self.add_button = QPushButton("Добавить товар")
        self.browse_button.setStyleSheet("color: white; background-color: blue")
        self.add_button.setStyleSheet("color: white; background-color: rgb(0, 220, 106)")

        font = QFont()
        font.setPointSize(12)
        self.browse_button.setFont(font)
        self.add_button.setFont(font)
        self.name_edit.setFont(font)
        self.price_edit.setFont(font)

        layout = QVBoxLayout()

        label_name = QLabel("Название товара:")
        label_name.setFont(font)
        layout.addWidget(label_name)

        layout.addWidget(self.name_edit)

        label_price = QLabel("Цена товара:")
        label_price.setFont(font)
        layout.addWidget(label_price)

        layout.addWidget(self.price_edit)

        label_image = QLabel("Изображение:")
        label_image.setFont(font)
        layout.addWidget(label_image)

        layout.addWidget(self.image_label)

        self.error_label = QLabel('')
        self.error_label.setStyleSheet("color: red")
        self.error_label.setFont(font)
        layout.addWidget(self.error_label)

        layout.addWidget(self.browse_button)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        self.browse_button.clicked.connect(self.browse_image)
        self.add_button.clicked.connect(self.add_product)

    def browse_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg)")
        if filename:
            self.image_label.setText(os.path.basename(filename))
            self.image_path = filename

    def add_product(self):
        name = self.name_edit.text()
        price = self.price_edit.text()
        image = getattr(self, "image_path", "")

        # Проверяем, чтобы все поля были заполнены
        if name and price and image:
            # Копируем изображение в папку с изображениями
            image_filename = os.path.basename(image)
            destination_path = os.path.join(
                "pictures", image_filename)
            shutil.copyfile(image, destination_path)

            image = destination_path

            product = {"name": name, "price": int(price), "image": image}
            products.append(product)
            with open('system_file\\products.json', 'w', encoding='UTF-8') as file:
                json.dump(products, file, indent=2, ensure_ascii=False)

            self.close()
        else:
            self.error_label.setText('Заполните все поля')
