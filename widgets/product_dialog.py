import os
import sys
from typing import Dict

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog, QFileDialog, QApplication, QPushButton,
    QLabel, QVBoxLayout, QLineEdit
)

import qt_env  # noqa: F401
from database import get_abs_path


# Добавление товаров (Подраздел для работников)
class AddProductDialog(QDialog):
    """Добавление товаров (Подраздел для работников)"""
    product_added: pyqtSignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(400, 300)

        self.name_edit: QLineEdit = QLineEdit()
        self.price_edit: QLineEdit = QLineEdit()
        self.image_label: QLabel = QLabel("Изображение не выбрано")
        self.browse_button: QPushButton = QPushButton("Выбрать изображение")
        self.add_button: QPushButton = QPushButton("Добавить товар")
        self.error_label: QLabel = QLabel('')

        self.image_path: str = ""  # путь к изображению

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Настройка UI элементов"""
        font = QFont()
        font.setPointSize(14)

        self.browse_button.setFont(font)
        self.add_button.setFont(font)
        self.name_edit.setFont(font)
        self.price_edit.setFont(font)
        self.error_label.setFont(font)
        self.error_label.setStyleSheet("color: red")

        self.browse_button.setStyleSheet("color: white; background-color: blue")
        self.add_button.setStyleSheet("color: white; background-color: rgb(0, 220, 106)")

        layout = QVBoxLayout()

        # Название
        label_name = QLabel("Название товара:")
        label_name.setFont(font)
        layout.addWidget(label_name)
        layout.addWidget(self.name_edit)

        # Цена
        label_price = QLabel("Цена товара:")
        label_price.setFont(font)
        layout.addWidget(label_price)
        layout.addWidget(self.price_edit)

        # Изображение
        label_image = QLabel("Изображение:")
        label_image.setFont(font)
        layout.addWidget(label_image)
        layout.addWidget(self.image_label)

        # Ошибки
        layout.addWidget(self.error_label)

        # Кнопки
        layout.addWidget(self.browse_button)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def _connect_signals(self) -> None:
        """Подключение сигналов к слотам"""
        self.browse_button.clicked.connect(self.browse_image)
        self.add_button.clicked.connect(self.add_product)

    def browse_image(self) -> None:
        """Выбор изображения"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            get_abs_path(),  # папка по умолчанию
            "Images (*.png *.jpg)"
        )
        if filename:
            self.image_label.setText(os.path.basename(filename))
            self.image_path = filename

    def add_product(self) -> None:
        name: str = self.name_edit.text().strip()
        price_text: str = self.price_edit.text().strip()
        image: str = self.image_path

        if not (name and price_text and image):
            self.error_label.setText('Заполните все поля!')
            return

        try:
            price: int = int(price_text)
        except ValueError:
            self.error_label.setText('Цена должна быть числом!')
            return

        product: Dict[str, object] = {"name": name, "price": price, "image": image}
        self.product_added.emit(product)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddProductDialog()
    window.show()
    sys.exit(app.exec())
