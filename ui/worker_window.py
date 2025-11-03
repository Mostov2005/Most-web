import sys
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.uic import loadUi

from database import DataBaseProductManager, get_abs_path
from widgets import AddProductDialog


class WorkerWindow(QMainWindow):
    """Окно для работников магазина"""
    back_signal = pyqtSignal()

    def __init__(self, database_product_manager: DataBaseProductManager):
        super().__init__()
        ui_path = get_abs_path("system_file", 'for_workers.ui')
        loadUi(ui_path, self)
        self.move(0, 0)

        self.database_product_manager = database_product_manager

        # Кнопки
        self.delete_btn.clicked.connect(self.delete_product)
        self.add_product_btn.clicked.connect(self.open_add_product_dialog)
        self.back_menu_btn.clicked.connect(self.switch_of_main)

        # Настройка таблицы
        self.table.setColumnCount(4)
        self.table.setColumnHidden(3, True)  # Скрытый столбец с ID
        self.table.setColumnWidth(0, 250)  # Название
        self.table.setColumnWidth(1, 150)  # Цена
        self.table.setColumnWidth(2, 536)  # Изображение

        self.populate_table()

    def populate_table(self):
        """Заполняет таблицу товарами из базы данных"""
        self.table.setRowCount(0)
        products = self.database_product_manager.get_products()

        for i, row in products.iterrows():
            table_row = self.table.rowCount()
            self.table.insertRow(table_row)

            self.table.setItem(table_row, 0, QTableWidgetItem(str(row['name'])))
            self.table.setItem(table_row, 1, QTableWidgetItem(str(row['price'])))
            self.table.setItem(table_row, 2, QTableWidgetItem(str(row['image'])))
            self.table.setItem(table_row, 3, QTableWidgetItem(str(row.name)))  # ID
            self.table.setColumnHidden(3, True)

    def delete_product(self):
        """Удаляет выбранный продукт"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите продукт для удаления.")
            return

        row_index = selected_items[0].row()
        id_item = self.table.item(row_index, 3)
        id_delete_product = int(id_item.text())

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f'Вы уверены, что хотите удалить товар "{selected_items[0].text()}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row_index)
            self.database_product_manager.delete_product(id_delete_product)

    def open_add_product_dialog(self):
        """Открывает диалог добавления нового продукта"""
        dialog = AddProductDialog(self)
        dialog.product_added.connect(self.add_product)
        dialog.exec()

    def add_product(self, product):
        """Добавляет продукт в базу и обновляет таблицу"""
        self.database_product_manager.add_product(product['name'],
                                                  product['price'],
                                                  product['image'])
        self.populate_table()

    def switch_of_main(self):
        """Возврат к главному окну"""
        self.back_signal.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_product_manager = DataBaseProductManager()

    worker_window = WorkerWindow(database_product_manager)
    worker_window.show()
    sys.exit(app.exec())
