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

# Для работников

class SetingForWorkers(QMainWindow):
    table_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        loadUi("system_file\\for_workers.ui", self)
        self.move(0, 0)

        # Подключаем сигнал к слоту для открытия окна добавления товара
        self.add_product_btn.clicked.connect(self.open_add_product_dialog)
        self.delete_btn.clicked.connect(self.delete_product)
        self.back_menu_btn.clicked.connect(self.switch_of_main)

        # Размеры таблицы
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 536)

        self.populate_table()

    def open_add_product_dialog(self):
        dialog = AddProductDialog(self)
        dialog.exec()
        self.populate_table()

    def populate_table(self):
        # Очищаем таблицу
        self.table.setRowCount(0)

        for row, item in enumerate(products):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(item["price"])))
            self.table.setItem(row, 2, QTableWidgetItem(item["image"]))

    def delete_product(self):
        global basket, summ_basket
        # Получаем список выбранных элементов
        selected_items = self.table.selectedItems()
        name_tovarr = selected_items[0].text()

        if selected_items:
            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f'Вы уверены, что хотите удалить товар "{selected_items[0].text()}"?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                selected_row = selected_items[0].row()
                self.table.removeRow(selected_row)

                image_path = products[selected_row]["image"]
                if os.path.exists(image_path):
                    os.remove(image_path)

                while name_tovarr in basket:
                    basket.remove(name_tovarr)
                    summ_basket -= int(products[selected_row]["price"])

                del products[selected_row]
                with open('system_file\\products.json', 'w', encoding='UTF-8') as file:
                    json.dump(products, file, indent=2, ensure_ascii=False)

        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите продукт для удаления.")

    def switch_of_main(self):
        self.hide()
        self.table_updated.emit()
        main_window.show()
