from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

import qt_env  # noqa: F401


class ProductWidget(QWidget):
    """
    Виджет для отображения одного продукта с изображением, названием,
    ценой и кнопкой добавления в корзину.
    """
    add_product_basket = pyqtSignal(int)

    def __init__(
        self,
        id_product: int,
        name: str,
        price: float,
        image_path: str,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)

        self.id_product: int = id_product

        layout = QVBoxLayout()

        font = QFont("Arial", 14)

        # Название продукта
        self.name_label = QLabel(name)
        self.name_label.setFont(font)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label)

        # Изображение продукта
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(300, 400, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)

        self.image_label.setStyleSheet("""
            border-radius: 10px;
            border: 6px solid rgb(92, 83, 220);
        """)
        self.image_label.setPixmap(pixmap)
        layout.addWidget(self.image_label)

        # Цена продукта
        self.price_label = QLabel(f"{price} ₽")
        self.price_label.setFont(font)
        self.price_label.setStyleSheet("color: rgb(167, 58, 253); font-weight: bold;")
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.price_label)

        # Кнопка покупки
        self.buy_button = QPushButton("Добавить в корзину")
        self.buy_button.setFont(font)
        self.buy_button.setFixedSize(280, 30)
        self.buy_button.clicked.connect(lambda: self.add_product_basket.emit(self.id_product))
        self.buy_button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                color: white;
                background-color: rgb(92, 83, 220);
            }
            QPushButton:hover {
                background-color: rgb(73, 17, 127);
            }
            QPushButton:pressed {
                background-color: rgb(50, 0, 100);
            }
        """)
        layout.addWidget(self.buy_button)

        self.setLayout(layout)
