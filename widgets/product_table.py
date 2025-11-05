import os
import sys
from typing import List, Dict, Any

from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget

import qt_env  # noqa: F401
from core import Recommender
from database import DataBaseProductManager
from widgets.product_widget import ProductWidget


class ProductTable(QObject):
    """
    Класс для управления таблицей продуктов в QTableWidget.
    """
    add_product_in_basket_signal = pyqtSignal(int)

    def __init__(self, table_widget: QTableWidget) -> None:
        super().__init__()
        self.table_widget: QTableWidget = table_widget

    def update_table(self, products: List[Dict[str, Any]]) -> None:
        """
        Обновляет таблицу виджетами продуктов.

        :param products: Список продуктов (каждый продукт - словарь)
        """
        self.table_widget.clear()

        count_col = min(4, len(products))  # максимум 4 колонки
        count_row = len(products) // 4 + (1 if len(products) % 4 != 0 else 0)

        self.table_widget.setRowCount(count_row)
        self.table_widget.setColumnCount(count_col)

        # Размер колонок и строк
        for i in range(count_col):
            self.table_widget.setColumnWidth(i, 300)
        for i in range(count_row):
            self.table_widget.setRowHeight(i, 500)

        # Заполнение таблицы виджетами продуктов
        for idx, product in enumerate(products):
            row = idx // 4
            col = idx % 4

            file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', product.get("image", ""))
            )

            widget = ProductWidget(
                product.name,
                product.get("name", ""),
                product.get("price", 0),
                file_path,
                self.table_widget
            )
            widget.add_product_basket.connect(self.add_product_in_basket)

            self.table_widget.setCellWidget(row, col, widget)

        # Настройки таблицы
        self.table_widget.horizontalHeader().setVisible(False)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_widget.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def add_product_in_basket(self, product_id: int) -> None:
        """
        Активирует сигнал добавления продукта в корзину.

        :param product_id: ID продукта
        """
        self.add_product_in_basket_signal.emit(product_id)


class TestProductWindow(QMainWindow):
    """
    Главное окно приложения с таблицей продуктов.
    """

    def __init__(self, database_product_manager: DataBaseProductManager) -> None:
        super().__init__()
        self.setWindowTitle("Товары")
        self.setGeometry(100, 100, 1300, 800)

        self.table_widget: QTableWidget = QTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.database_product_manager: DataBaseProductManager = database_product_manager
        self.recommender: Recommender = Recommender(self.database_product_manager)

        products_id: List[int] = self.recommender.get_recommendation_products_id()
        self.products: List[Dict[str, Any]] = self.database_product_manager.get_products_by_id(products_id)

        self.product_table: ProductTable = ProductTable(self.table_widget)
        self.product_table.update_table(self.products)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_product_manager = DataBaseProductManager()
    window = TestProductWindow(database_product_manager)
    window.show()
    sys.exit(app.exec())
