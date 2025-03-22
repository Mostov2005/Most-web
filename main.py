import json
import sys
import hashlib
import re
import os
import shutil

from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QRect, QEasingCurve, Qt, QRegularExpression
from PyQt6.QtGui import QPixmap, QIntValidator, QFont, QRegularExpressionValidator
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QRadioButton, QButtonGroup, QComboBox, QFileDialog
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QMainWindow, QMessageBox, QLineEdit


# Хешер паролей(для регистрации)
class PasswordHasher:
    def hash_password(self, password: str) -> str:
        hash_object = hashlib.sha256()
        hash_object.update(password.encode())
        hashed_password = hash_object.hexdigest()

        return hashed_password


# Вход
class WelcomeWindow(QMainWindow):
    # Определяем кастомный сигнал
    name_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        loadUi("system_file\\welcome.ui", self)

        self.registr_btn.clicked.connect(self.switch_on_registr)
        self.avt_btn.clicked.connect(self.authorization)
        self.name_edit.textChanged.connect(self.clear_error_message)
        self.paroll_edit.textChanged.connect(self.clear_error_message)

        self.name_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paroll_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def authorization(self):
        self.name = self.name_edit.text()
        password = PasswordHasher().hash_password(self.paroll_edit.text())
        if self.name not in users:
            self.error_label.setText("Неверное имя пользователя или пароль!")
        else:
            if password == users[self.name][1]:
                # Передаем имя пользователя через сигнал
                self.switch_on_main()
            else:
                self.error_label.setText("Неверное имя пользователя или пароль!")

    def clear_error_message(self):
        self.error_label.clear()

    def switch_on_registr(self):
        self.name_edit.clear()
        self.paroll_edit.clear()
        self.error_label.clear()
        registr_window.show()
        self.close()

    def switch_on_main(self):
        name = self.name
        self.name_updated.emit(name)  # Активируем сигнал
        main_window.show()  # Показываем главное окно
        self.close()  # Закрываем текущее окно


# Регистрация
class RegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("system_file\\registration.ui", self)

        self.back_btn.clicked.connect(self.switch_on_welcome)
        # Установка выравнивания для полей ввода
        self.login_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.email_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phone_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paroll_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paroll_return_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Подключение слотов к событиям изменения текста
        self.login_edit.textChanged.connect(self.login_valid)
        self.email_edit.textChanged.connect(self.valid_email)
        self.paroll_edit.textChanged.connect(self.valid_paroll)
        self.paroll_return_edit.textChanged.connect(self.valid_return_paroll)

        self.flag_login = False
        self.flag_email = False
        self.flag_phone = False
        self.flag_paroll = False
        self.flag_return_paroll = False

        # Подключение слота к кнопке регистрации
        self.registr_btn.clicked.connect(self.valid_regist)

        # Установка маски и игнорирование события для поля ввода номера телефона
        self.phone_edit.setPlaceholderText("+7 (___) ___-__-__")
        self.phone_edit.setInputMask("+7 (999) 999-99-99")
        self.phone_edit.mousePressEvent = self.ignore_event
        self.phone_edit.textChanged.connect(self.valid_phone)

        # Установка валидатора для поля ввода email
        email_validator = QRegularExpressionValidator(
            QRegularExpression(r'^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$'), self.email_edit)
        self.email_edit.setValidator(email_validator)

    def clear_fields(self):
        self.login_edit.clear()
        self.email_edit.clear()
        self.phone_edit.clear()
        self.paroll_edit.clear()
        self.paroll_return_edit.clear()

        self.error_login_label.clear()
        self.error_email_label.clear()
        self.error_parol_label.clear()
        self.error_phone_label.clear()
        self.error_return_paroll_label.clear()
        self.error_registration_label.clear()

    def switch_on_welcome(self):
        welcome_window.show()
        self.clear_fields()
        self.close()

    def ignore_event(self, event):
        pass

    def login_valid(self, text):
        self.flag_login = False
        self.error_login_label.clear()  # Очищаем сообщение об ошибке
        self.error_registration_label.clear()
        if len(text) < 5:
            self.error_login_label.setText('Логин должен состоять не менее чем из 5 символов')
        elif re.search(r'[^a-zA-Z0-9]', text):
            self.error_login_label.setText('В логине могут использоваться только буквы латинского алфавита и цифры')
        elif self.login_edit.text() in users:
            self.error_login_label.setText('Пользователь с таким логином уже существует')
        else:
            self.flag_login = True

    def valid_email(self, text):
        self.flag_email = False
        self.error_email_label.clear()
        self.error_registration_label.clear()
        if not self.email_edit.hasAcceptableInput():
            self.error_email_label.setText("Введен некорректный email")
        for user in users.values():
            if self.email_edit.text() == user[2]:
                self.error_email_label.setText('Пользователь с таким email уже существует')
        else:
            self.flag_email = True

    def valid_phone(self, text):
        self.flag_phone = False
        self.error_phone_label.clear()
        self.error_registration_label.clear()
        if len(text) < 18:
            self.error_phone_label.setText('Неверно введен номер телефона')
        for user in users.values():
            if self.phone_edit.text() == user[3]:
                self.error_phone_label.setText('Пользователь с таким номером телефона уже существует')
        else:
            self.flag_phone = True

    def valid_paroll(self, text):
        self.flag_paroll = False
        self.error_parol_label.clear()
        self.error_registration_label.clear()
        if len(text) < 8:
            self.error_parol_label.setText('Пароль должен состоять не менее чем из 8 символов')

        elif not re.search('[a-z]', text):
            self.error_parol_label.setText(
                'Пароль должен содержать как минимум одну строчную букву латинского алфавита')

        elif not re.search('[A-Z]', text):
            self.error_parol_label.setText(
                'Пароль должен содержать как минимум одну прописную букву латинского алфавита')

        elif not re.search('[0-9]', text):
            self.error_parol_label.setText('Пароль должен содержать хотя бы одну цифру')

        elif not re.search('[!@#$%^&*(),.?":{}|<>_-]', text):
            self.error_parol_label.setText('Пароль должен содержать хотя бы один специальный символ')

        else:
            self.flag_paroll = True

    def valid_return_paroll(self, text):
        self.flag_return_paroll = False
        self.error_return_paroll_label.clear()
        self.error_registration_label.clear()
        if text != self.paroll_edit.text():
            self.error_return_paroll_label.setText('Пароли не совпадают')
        else:
            self.flag_return_paroll = True

    def valid_regist(self):
        self.error_registration_label.clear()
        if not (all([self.flag_login, self.flag_email, self.flag_phone, self.flag_paroll, self.flag_return_paroll])):
            self.error_registration_label.setText('Заполните все поля для регистрации')

        else:
            login = (self.login_edit.text())
            email = (self.email_edit.text())
            phone = (self.phone_edit.text())
            status = 'Buyer'
            balans = 0
            password = PasswordHasher().hash_password(self.paroll_edit.text())
            polzovael = []
            polzovael.append(login), polzovael.append(password), polzovael.append(email), polzovael.append(
                phone), polzovael.append(status), polzovael.append(balans)
            print(polzovael)
            users[login] = polzovael
            with open('system_file\\users.json', 'w') as file:
                json.dump(users, file, ensure_ascii=False, indent=2)

            self.switch_on_welcome()


# Заполнение таблицы(Подраздел главного окна)
class ProductWidget(QWidget):
    def __init__(self, name, price, image_path, parent=None):
        super(ProductWidget, self).__init__(parent)
        layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(14)
        font.setFamily("Arial")

        self.name_label = QLabel(name)
        self.name_label.setFont(font)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label)

        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(300, 400, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)

        self.image_label.setStyleSheet("""
            border-radius: 10px;
            border: 6px solid rgb(92, 83, 220);
        """)
        self.image_label.setPixmap(pixmap)

        layout.addWidget(self.image_label)

        self.price_label = QLabel(f"{price} ₽")
        self.price_label.setFont(font)
        self.price_label.setStyleSheet("color: rgb(167, 58, 253); font-weight: bold;")
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.price_label)

        self.buy_button = QPushButton("Добавить в корзину")
        self.buy_button.clicked.connect(lambda: self.add_tovar_in_basket(name, price))
        self.buy_button.setFont(font)
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
        self.buy_button.setFixedSize(280, 30)
        layout.addWidget(self.buy_button)

        self.setLayout(layout)

    def add_tovar_in_basket(self, name_tovar, price):
        global summ_basket
        basket.append(name_tovar)
        summ_basket += price
        main_window.update_basket_label()


# Боковое меню(Подраздел главного окна)
class SlidingMenu(QWidget):
    def __init__(self, parent=None, main_window=None):
        super(SlidingMenu, self).__init__(parent)
        self.main_window = main_window  # Store the reference to MainWindow

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(-350, 350, 350, 990)  # Initial position off-screen

        # Create a container widget for border
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 350, 990)
        self.container.setStyleSheet(
            "background-color: #e6deff; border-radius: 10px; border: 6px solid rgb(92, 83, 220);"
        )

        # Create the main widget for control elements
        self.content = QWidget(self)
        self.content.setGeometry(0, 0, 350, 990)
        self.content.setStyleSheet("background-color: transparent;")  # Transparent background

        # Add text "Фильтры"
        label_filters = QLabel("Фильтры", self.content)
        label_filters.setGeometry(100, 25, 150, 30)
        label_filters.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_filters.setStyleSheet("font-size: 26px; font-family: 'Arial';")

        label_filter = QLabel("Сортировать по:", self.content)
        label_filter.setGeometry(13, 70, 150, 30)
        label_filter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_filter.setStyleSheet("font-size: 20px; font-family: 'Arial';")

        # Add radio buttons for filters
        radio1 = QRadioButton("Цене убывание", self.content)
        radio1.setGeometry(13, 110, 150, 30)
        radio1.setStyleSheet("font-size: 16px; font-family: 'Arial';")

        radio2 = QRadioButton("Цене возрастание", self.content)
        radio2.setGeometry(13, 145, 200, 30)
        radio2.setStyleSheet("font-size: 16px; font-family: 'Arial';")

        radio3 = QRadioButton("По названию", self.content)
        radio3.setGeometry(13, 180, 150, 30)
        radio3.setStyleSheet("font-size: 16px; font-family: 'Arial';")

        radio_group = QButtonGroup(self)
        radio_group.addButton(radio1)
        radio_group.addButton(radio2)
        radio_group.addButton(radio3)

        self.label_worker = QLabel("Для работников", self.content)
        self.label_worker.setStyleSheet("font-size: 20px; font-family: 'Arial';")
        self.label_worker.setGeometry(100, 300, 150, 30)
        self.label_worker.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add button for worker
        self.button_worker = QPushButton("Меню товаров", self.content)
        self.button_worker.setGeometry(50, 350, 250, 40)
        self.button_worker.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                color: white;
                background-color: rgb(0, 0, 255);
                font-size: 16px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: rgb(0, 0, 158);
            }
        """)
        self.button_worker.clicked.connect(self.main_window.switch_to_worker_menu)

        # Add text "Для администратора"
        self.label_admin = QLabel("Для администраторов", self.content)
        self.label_admin.setGeometry(77, 500, 204, 30)  # Set coordinates and sizes
        self.label_admin.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center alignment
        self.label_admin.setStyleSheet("font-size: 20px; font-family: 'Arial';")  # Set font size

        # Add button for administrator
        self.button_admin = QPushButton("Меню администратора", self.content)
        self.button_admin.setGeometry(50, 550, 250, 40)  # Set coordinates and sizes
        self.button_admin.clicked.connect(self.main_window.switch_of_for_admin)
        self.button_admin.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                color: white;
                background-color: rgb(0, 0, 255);
                font-size: 16px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: rgb(0, 0, 158);
            }
        """)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)  # Reduce animation duration
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)  # Smooth animation

    def slide_in(self):
        start_rect = self.geometry()
        end_rect = QRect(0, 0, 350, 990)
        self.animate(start_rect, end_rect)

    def slide_out(self):
        start_rect = self.geometry()
        end_rect = QRect(-350, 350, 350, 990)
        self.animate(start_rect, end_rect)

    def animate(self, start_rect, end_rect):
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()

    def hide_btn(self, status):
        if status == 'Buyer':
            self.label_admin.hide()
            self.button_admin.hide()
            self.label_worker.hide()
            self.button_worker.hide()
        elif status == 'Worker':
            self.label_admin.hide()
            self.button_admin.hide()


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

                        with open('system_file\\users.json', 'w') as file:
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


# Подраздел главного окна(пополнение баланса)
class Poplnenie_balansa(QMainWindow):
    balance_updated = pyqtSignal(str)

    def __init__(self, name):
        super().__init__()
        loadUi("system_file\\plus_balans.ui", self)
        self.move(0, 0)

        self.poplnenie_btn.clicked.connect(self.add_summ)
        self.back_menu_btn.clicked.connect(self.swith_of_main)

        self.name_polzovatel = name
        self.tec_balans = users[self.name_polzovatel][5]
        self.label_tec_balans.setText(f'Текущий баланс: {self.tec_balans}')
        self.label_tec_balans.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line_add_summ.setValidator(self.positive_int_validator())
        self.line_add_summ.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Загружаем изображение
        pixmap = QPixmap("system_file\\my_QR.png")
        pixmap = pixmap.scaled(375, 375, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)
        # Устанавливаем изображение на QLabel
        self.label_image.setPixmap(pixmap)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("""
                    border-radius: 10px;
                    border: 6px solid rgb(92, 83, 220);
                """)

    def positive_int_validator(self):
        validator = QIntValidator()
        validator.setBottom(1)  # Устанавливаем минимальное значение, чтобы не было нуля и отрицательных чисел
        return validator

    def add_summ(self):
        if len(self.line_add_summ.text()) > 0:
            plus_summ = int(self.line_add_summ.text())
            self.line_add_summ.clear()
            self.tec_balans += plus_summ

            self.label_tec_balans.setText(f'Текущий баланс: {self.tec_balans}')

            users[self.name_polzovatel][5] = self.tec_balans
            with open('system_file\\users.json', 'w') as file:
                json.dump(users, file, ensure_ascii=False, indent=2)

            # Emit signal
            self.balance_updated.emit(self.name_polzovatel)

    def swith_of_main(self):
        self.hide()
        main_window.show()


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
                with open('system_file\\users.json', 'w', encoding='UTF-8') as file:
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
        with open('system_file\\users.json', 'w') as file:
            json.dump(users, file, indent=2)

    def swith_of_main(self):
        self.hide()
        main_window.show()


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


if __name__ == "__main__":
    global basket, summ_basket
    basket = []
    summ_basket = 0
    try:
        with open('system_file\\products.json', 'r', encoding='UTF-8') as file:
            products = json.load(file)
    except json.decoder.JSONDecodeError:
        products = []
    try:
        with open('system_file\\users.json', 'r', encoding='UTF-8') as file:
            users = json.load(file)
    except json.decoder.JSONDecodeError:
        users = {}

    app = QApplication(sys.argv)

    main_window = MainWindow()
    welcome_window = WelcomeWindow()
    registr_window = RegistrationWindow()

    welcome_window.name_updated.connect(main_window.update_balance_label)

    welcome_window.show()
    sys.exit(app.exec())
