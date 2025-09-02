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


# Главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("system_file\\main_window.ui", self)
        # self.setWindowState(Qt.WindowFullScreen)
        self.move(0, 0)
        self.basket_window = None

        self.name = 'Mostov'
        self.menu = SlidingMenu(self, self)  # Pass self to SlidingMenu
        self.toggle_btn.clicked.connect(self.toggle_menu)

        self.poisk_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.basket_btn.clicked.connect(self.switch_to_basket)
        self.popolnenie_balans_btn.clicked.connect(self.switch_to_plus_balance)

        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)

        self.update_table()
        # self.update_balance_label()

    def toggle_menu(self):
        if self.menu.geometry().x() < 0:
            self.menu.slide_in()
        else:
            self.menu.slide_out()

    def update_table(self):
        self.tableWidget.setRowCount(0)
        count_cow = min(4, len(products))
        count_row = len(products) // 4 + 1
        self.tableWidget.setRowCount(count_row)
        self.tableWidget.setColumnCount(count_cow)

        for i in range(count_cow):
            self.tableWidget.setColumnWidth(i, 300)

        for i in range(count_row):
            self.tableWidget.setRowHeight(i, 500)

        # Fill table
        for idx, product in enumerate(products):
            row = idx // 4
            col = idx % 4
            product_widget = ProductWidget(product['name'], product['price'], product['image'], self)
            self.tableWidget.setCellWidget(row, col, product_widget)

        self.update_basket_label()

    def switch_of_for_admin(self):
        self.for_admin_window = SetingForAdmin(self.name)
        self.close()
        self.for_admin_window.show()

    def switch_to_worker_menu(self):
        self.for_workers_window = SetingForWorkers()
        self.for_workers_window.table_updated.connect(self.update_table)
        self.close()
        self.for_workers_window.show()

    def update_basket_label(self):
        self.count_tovar_label.setText(f'{len(basket)}: {summ_basket} ₽')
        self.count_tovar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.popolnenie_balans_btn.setText(f'+ {users[self.name][5]}₽')

    def update_balance_label(self, name):
        self.name = name
        self.name_label.setText(self.name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.popolnenie_balans_btn.setText(f'+ {users[self.name][5]}₽')
        self.status = users[self.name][4]
        self.menu.hide_btn(self.status)
        self.update_basket_label()

    def switch_to_basket(self):
        self.basket_window = Oformalenie_Zakaza(self.name)
        self.basket_window.basket_updated.connect(self.update_basket_label)
        self.close()
        self.basket_window.show()

    def switch_to_plus_balance(self):
        self.plus_balans = Poplnenie_balansa(self.name)
        self.plus_balans.balance_updated.connect(self.update_balance_label)
        self.close()
        self.plus_balans.show()
