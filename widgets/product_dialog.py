import os
import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog, QFileDialog, QApplication
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QLineEdit
from database import get_abs_path


# Добавление товаров(Подраздел для работников)
class AddProductDialog(QDialog):
    product_added = pyqtSignal(dict)

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
        font.setPointSize(14)
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
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            get_abs_path(),  # папка по умолчанию
            "Images (*.png *.jpg)"
        )
        if filename:
            self.image_label.setText(os.path.basename(filename))
            self.image_path = filename

    def add_product(self):
        name = self.name_edit.text()
        price = self.price_edit.text()
        image = getattr(self, "image_path", "")

        # Проверяем, чтобы все поля были заполнены
        if name and price and image:
            product = {"name": name, "price": int(price), "image": image}
            self.product_added.emit(product)

            self.close()
        else:
            self.error_label.setText('Заполните все поля!')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddProductDialog()
    window.show()
    sys.exit(app.exec())
