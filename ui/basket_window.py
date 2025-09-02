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


# Подраздел главного окна(Корзина)
class Oformalenie_Zakaza(QMainWindow):
    basket_updated = pyqtSignal(str)  # Определяем кастомный сигнал

    def __init__(self, name):
        super().__init__()
        loadUi("system_file\\oformlenie_zakaza.ui", self)
        self.name = name
        self.move(0, 0)

        self.back_menu_btn.clicked.connect(self.swith_of_main)
        self.oformlenie_zakaza_btn.clicked.connect(self.oformlenie_zakaza)

        self.balans = str(users[self.name][5])

        self.name_label.setText(self.name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.balans_label.setText(f'Баланс: {self.balans}₽')
        self.balans_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.font = QFont()
        self.font.setPointSize(16)

        # Подключаем сигнал к слоту для удаления товара
        self.delete_btn.clicked.connect(self.delete_product)

        # Размеры таблицы
        self.table.setColumnWidth(0, 72)
        self.table.setColumnWidth(1, 573)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 200)

        self.populate_table()

    def populate_table(self):
        # Создаем словарь, где ключами будут названия товаров, а значениями - их индексы в списке products
        product_index = {product['name']: index for index, product in enumerate(products)}
        # Создаем словарь корзины, используя словарь product_index для быстрого поиска индексов товаров
        basket_dict = {item: product_index[item] for item in basket if item in product_index}

        # Очищаем таблицу
        self.table.setRowCount(0)

        for row, item in enumerate(sorted(set(basket))):
            self.table.insertRow(row)
            self.table.setRowHeight(row, 120)

            pixmap = QPixmap(products[basket_dict[item]]['image'])
            pixmap = pixmap.scaled(72, 120, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)

            image_label = QLabel()
            image_label.setPixmap(pixmap)
            self.table.setCellWidget(row, 0, image_label)

            name_item = QTableWidgetItem(item)
            name_item.setFont(self.font)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, name_item)

            count_item = QTableWidgetItem(str(basket.count(item)))
            count_item.setFont(self.font)
            count_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, count_item)

            price_item = QTableWidgetItem(str(products[basket_dict[item]]['price']) + '₽')
            price_item.setFont(self.font)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, price_item)

        self.itog_label.setText(f'Итого: {str(summ_basket)}₽')
        self.itog_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def delete_product(self):
        global basket
        global summ_basket
        selected_items = self.table.selectedItems()
        if selected_items:
            # Получаем имя товара из второй колонки (индекс 1)
            item_name = self.table.item(selected_items[0].row(), 1).text()
            price_item = self.table.item(selected_items[0].row(), 3).text()
            summ_basket -= int(price_item[:-1])
            # Удаляем первый найденный элемент с таким именем из basket
            basket.remove(item_name)
            # Обновляем таблицу после удаления элемента
            self.populate_table()
            # Эмитируем сигнал
            self.basket_updated.emit(self.name)
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите продукт для удаления.")

    def oformlenie_zakaza(self):
        global basket, summ_basket

        if len(basket) == 0:
            warning_dialog = QDialog()
            warning_dialog.setStyleSheet("""
                QDialog {
                    background-color: white;
                }
                """)
            warning_dialog.setWindowTitle("Ошибка!")
            warning_dialog.setGeometry(810, 490, 300, 100)
            warning_layout = QVBoxLayout()
            warning_label = QLabel("Ваша корзина пуста!", warning_dialog)
            warning_label.setStyleSheet('background-color: white')
            warning_label.setFont(QFont("Arial", 12))
            warning_layout.addWidget(warning_label, alignment=Qt.AlignmentFlag.AlignCenter)
            warning_dialog.setLayout(warning_layout)
            warning_dialog.exec()

        else:

            if int(self.balans) < summ_basket:
                dialog = QDialog(self)
                dialog.setWindowTitle("Ой!")
                dialog.setGeometry(630, 465, 300, 150)
                dialog.setStyleSheet("""
                    QDialog {
                        background-color: white;
                    }
                    """)

                layout = QVBoxLayout()
                # Добавляем текст
                label = QLabel("К сожалению, на вашем счете недостаточно средств для совершения данной операции.",
                               dialog)
                label.setStyleSheet('background-color: white')
                # Устанавливаем шрифт для QLabel
                font = QFont("Arial", 12)
                label.setFont(font)
                layout.addWidget(label)
                # Добавляем пользовательскую кнопку
                custom_button = QPushButton("Пополнить баланс", dialog)
                custom_button.setStyleSheet("""
                                QPushButton {
                                    border-radius: 10px;
                                    color: white;
                                    background-color: rgb(0, 220, 106);
                                    padding: 10px;
                                }
                                QPushButton:hover {
                                    background-color: rgb(0, 152, 0);
                                }
                            """)

                custom_button.clicked.connect(lambda: self.switch_of_poplnenie_balans(dialog))
                layout.addWidget(custom_button, alignment=Qt.AlignmentFlag.AlignCenter)

                dialog.setLayout(layout)
                dialog.exec()

            else:
                dialog = QDialog(self)
                dialog.setWindowTitle("Оформление заказа")
                dialog.setGeometry(710, 465, 500, 150)
                dialog.setStyleSheet("""
                    QDialog {
                        background-color: white;
                    }
                    """)

                layout = QVBoxLayout()
                # Добавляем текст
                label_1 = QLabel("Укажите адрес доставки:", dialog)
                label_1.setStyleSheet('background-color: white')
                label_1.setFont(QFont("Arial", 12))
                layout.addWidget(label_1)

                # Поле для ввода адреса
                line_edit = QLineEdit(dialog)
                line_edit.setFont(QFont("Arial", 12))
                line_edit.setStyleSheet('background-color: white')
                layout.addWidget(line_edit)

                # Добавляем пользовательскую кнопку
                custom_button = QPushButton("Оформить заказ", dialog)
                custom_button.setStyleSheet("""
                                QPushButton {
                                    border-radius: 10px;
                                    color: white;
                                    background-color: rgb(0, 220, 106);
                                    padding: 10px;
                                }
                                QPushButton:hover {
                                    background-color: rgb(0, 152, 0);
                                }
                            """)

                def on_order_click():
                    global basket, summ_basket
                    if not line_edit.text().strip():
                        QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите адрес доставки.")
                    else:
                        users[self.name][5] -= summ_basket
                        basket.clear()
                        summ_basket = 0

                        with open('system_file\\users.csv', 'w') as file:
                            json.dump(users, file, ensure_ascii=False, indent=2)

                        dialog.accept()  # Закрываем диалог перед переходом на главный экран
                        QMessageBox.information(self, "Успех", "Ваш заказ успешно оформлен.")
                        self.swith_of_main()

                custom_button.clicked.connect(on_order_click)
                layout.addWidget(custom_button, alignment=Qt.AlignmentFlag.AlignCenter)

                dialog.setLayout(layout)
                dialog.exec()

    def swith_of_main(self):
        self.basket_updated.emit(self.name)
        self.hide()
        main_window.show()

    def switch_of_poplnenie_balans(self, dialog):
        self.plus_balans = Poplnenie_balansa(self.name)
        self.plus_balans.balance_updated.connect(main_window.update_balance_label)
        self.close()
        dialog.accept()
        self.plus_balans.show()
