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


# Для администраторов
class SetingForAdmin(QMainWindow):
    def __init__(self, name):
        super().__init__()
        loadUi("system_file\\for_admin.ui", self)
        self.move(0, 0)

        self.name = name

        self.font = QFont()
        self.font.setPointSize(12)

        self.delete_btn.clicked.connect(self.delete_user)
        self.save_btn.clicked.connect(self.save_edits)
        self.back_menu_btn.clicked.connect(self.swith_of_main)

        self.table_tec.setColumnWidth(0, 215)
        self.table_tec.setColumnWidth(1, 193)
        self.table_tec.setColumnWidth(2, 250)
        self.table_tec.setColumnWidth(3, 200)
        self.table_tec.setColumnWidth(4, 150)
        self.table_tec.setColumnWidth(5, 150)

        # Размеры таблицы
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 193)
        self.table.setColumnWidth(2, 250)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 150)

        self.populate_table_tec()
        self.populate_table()

    def populate_table(self):
        # Очищаем таблицу
        self.table.setRowCount(0)
        k = 0

        for row, item in enumerate(users):
            row -= k

            if item == self.name:
                k = 1
                continue
            self.table.insertRow(row)
            self.table.setColumnWidth(0, 200)
            for col, value in enumerate(users[item]):
                if col == 4:
                    combo_box = QComboBox()
                    combo_box.addItems(["Buyer", "Worker", "Admin"])
                    combo_box.setCurrentText(
                        str(value).strip())  # Используем str(value).strip() для удаления лишних пробелов
                    combo_box.setFont(self.font)  # Установите шрифт для QComboBox
                    combo_box.setStyleSheet("border: none;")
                    self.table.setCellWidget(row, col, combo_box)

                elif col == 5:
                    line_edit = QLineEdit()
                    line_edit.setValidator(QIntValidator())  # Устанавливаем валидатор для чисел
                    line_edit.setText(str(value))
                    line_edit.setFont(self.font)  # Установите шрифт для QLineEdit
                    line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрируем текст
                    self.table.setCellWidget(row, col, line_edit)

                else:
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if col == 1:
                        table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.table.setItem(row, col, table_item)

    def populate_table_tec(self):
        self.table_tec.setRowCount(0)  # Clear the table_tec
        self.table_tec.insertRow(0)
        user_data = users.get(self.name, [])  # Get the current user's data
        for col, value in enumerate(user_data):
            table_item = QTableWidgetItem(str(value))
            table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make it non-editable
            self.table_tec.setItem(0, col, table_item)  # Assuming table_tec has only one column

    def delete_user(self):
        global users
        selected_items = self.table.selectedItems()
        if selected_items:
            selected_row = selected_items[0].row()
            user_name = self.table.item(selected_row, 0).text()
            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Вы уверены, что хотите удалить пользователя {user_name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.table.removeRow(selected_row)
                del users[user_name]  # Удаление из списка пользователей
                self.table.setColumnWidth(0, 215)
                with open('system_file\\users.csv', 'w', encoding='UTF-8') as file:
                    json.dump(users, file, indent=2, ensure_ascii=False)
            else:
                pass
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите пользователя для удаления.")

    def save_edits(self):
        for row in range(self.table.rowCount()):
            username = self.table.item(row, 0).text()

            role_combo_box = self.table.cellWidget(row, 4)
            role = role_combo_box.currentText()
            balans_line_edit = self.table.cellWidget(row, 5)
            balans = balans_line_edit.text()

            user_data = [self.table.item(row, col).text() for col in range(0, 4)]
            user_data.append(role), user_data.append(int(balans))

            users[username] = user_data
        with open('system_file\\users.csv', 'w') as file:
            json.dump(users, file, indent=2)

    def swith_of_main(self):
        self.hide()
        main_window.show()
