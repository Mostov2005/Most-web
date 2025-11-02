import sys

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, \
    QPushButton, QLineEdit
from PyQt6.uic import loadUi

from database import DataBaseProductManager
from database import DataBaseUserManager
from database import DataBaseOrdersManager
from database import get_abs_path
from ui.balance_window import AddBalance


# Подраздел главного окна (Корзина)
class BasketWindow(QMainWindow):
    basket_updated = pyqtSignal(dict)

    def __init__(self, user_id, database_user_manager, database_product_manager, basket):
        super().__init__()
        ui_path = get_abs_path("system_file", 'oformlenie_zakaza.ui')
        loadUi(ui_path, self)

        self.move(0, 0)

        self.database_user_manager = database_user_manager
        self.database_product_manager = database_product_manager
        self.database_orders_manager = DataBaseOrdersManager()
        self.basket: dict[int, int] = basket
        self.user_id = user_id
        self.balans = 0
        self.name = ''
        self.summ_basket = 0

        self.font = QFont()
        self.font.setPointSize(16)

        self.back_menu_btn.clicked.connect(self.switch_of_main)
        self.oformlenie_zakaza_btn.clicked.connect(self.oformlenie_zakaza)

        self.delete_btn.clicked.connect(self.delete_product)

        self.table.setColumnCount(5)
        self.table.setColumnHidden(4, True)
        # Размеры таблицы
        self.table.setColumnWidth(0, 72)
        self.table.setColumnWidth(1, 573)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 200)

        self.update_label()

    def update_label(self):
        self.balans = self.database_user_manager.get_balance_by_id(user_id=self.user_id)
        self.name = self.database_user_manager.get_name_by_id(user_id=self.user_id)

        self.balans_label.setText(f'Баланс: {str(self.balans)}₽')
        self.balans_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name_label.setText(self.name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.populate_table()

    def populate_table(self):
        def create_item(text):
            item = QTableWidgetItem(text)
            item.setFont(self.font)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            return item

        self.summ_basket = 0
        # Очищаем таблицу
        self.table.setRowCount(0)

        for row_index, product_index in enumerate(self.basket):
            product = self.database_product_manager.get_info_product_by_id(product_index)

            name_product = product.get('name', '')
            price_product = product.get('price', 0)
            image_product = product.get('image', '')

            if name_product == '' or image_product == '' or price_product == 0:
                continue

            self.table.insertRow(row_index)
            self.table.setRowHeight(row_index, 120)

            # Работа с изображением
            pixmap = QPixmap(get_abs_path(image_product))
            pixmap = pixmap.scaled(72, 120, aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            self.table.setCellWidget(row_index, 0, image_label)

            self.table.setItem(row_index, 1, create_item(name_product))
            self.table.setItem(row_index, 2, create_item(str(self.basket[product_index])))
            self.table.setItem(row_index, 3, create_item(str(price_product) + '₽'))
            self.table.setItem(row_index, 4, QTableWidgetItem(str(product_index)))
            self.table.setColumnHidden(4, True)

            self.summ_basket += price_product * self.basket[product_index]

        self.itog_label.setText(f'Итого: {str(self.summ_basket)}₽')
        self.itog_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def delete_product(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите продукт для удаления.")
            return
        row_index = selected_items[0].row()
        id_item = self.table.item(row_index, 4)
        product_id = int(id_item.text())

        if self.basket.get(product_id, 0) > 1:
            self.basket[product_id] -= 1
        else:
            self.basket.pop(product_id, None)

        self.populate_table()

    def oformlenie_zakaza(self):
        # 1. Проверка корзины
        if self.is_basket_empty():
            self.show_warning_dialog("Ваша корзина пуста!", width=300, height=100)
            return

        # 2. Проверка баланса
        if self.balans < self.summ_basket:
            self.show_warning_dialog(
                "К сожалению, на вашем счете недостаточно средств для совершения данной операции.",
                width=300, height=150
            )
            return

        # 3. Основной диалог оформления заказа
        self.show_order_dialog()

    def is_basket_empty(self):
        return not self.basket

    def show_warning_dialog(self, message, width=300, height=100):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ошибка!" if "пуст" in message else "Ой!")
        dialog.setGeometry(810, 490, width, height)
        dialog.setStyleSheet("QDialog { background-color: white; }")

        layout = QVBoxLayout()
        label = QLabel(message, dialog)
        label.setStyleSheet("background-color: white")
        label.setFont(QFont("Arial", 12))
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        # custom_button = QPushButton("Пополнить баланс", dialog)
        # custom_button.setStyleSheet("""
        #                 QPushButton {
        #                     border-radius: 10px;
        #                     color: white;
        #                     background-color: rgb(0, 220, 106);
        #                     padding: 10px;
        #                 }
        #                 QPushButton:hover {
        #                     background-color: rgb(0, 152, 0);
        #                 }
        #             """)
        #
        # custom_button.clicked.connect(lambda: self.switch_of_add_balans(dialog))
        # layout.addWidget(custom_button, alignment=Qt.AlignmentFlag.AlignCenter)

        dialog.setLayout(layout)
        dialog.exec()

    def show_order_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Оформление заказа")
        dialog.setGeometry(710, 465, 500, 150)
        dialog.setStyleSheet("QDialog { background-color: white; }")

        layout = QVBoxLayout()

        # Адрес доставки
        label = QLabel("Укажите адрес доставки:", dialog)
        label.setFont(QFont("Arial", 12))
        layout.addWidget(label)
        line_edit = QLineEdit(dialog)
        line_edit.setFont(QFont("Arial", 12))
        layout.addWidget(line_edit)

        # Кнопка оформления
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
        custom_button.clicked.connect(lambda: self.confirm_order(dialog, line_edit))
        layout.addWidget(custom_button, alignment=Qt.AlignmentFlag.AlignCenter)

        dialog.setLayout(layout)
        dialog.exec()

    def confirm_order(self, dialog, line_edit):
        address = line_edit.text().strip()
        if not address:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите адрес доставки.")
            return

        # Списание средств
        self.database_user_manager.set_balance_by_id(
            user_id=self.user_id,
            new_balance=self.balans - self.summ_basket
        )

        for product, quantity in self.basket.items():
            self.database_orders_manager.write_row(product, self.user_id, quantity)
        self.database_orders_manager.save()

        self.basket.clear()
        self.update_label()

        dialog.accept()
        QMessageBox.information(self, "Успех", "Ваш заказ успешно оформлен.")

    # def switch_of_add_balans(self, dialog):
    #     self.plus_balans = AddBalance(self.database_user_manager, self.user_id)
    #     self.close()
    #     dialog.accept()
    #     self.plus_balans.show()

    def switch_of_main(self):
        self.basket_updated.emit(self.basket)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_product_manager = DataBaseProductManager()
    database_user_manager = DataBaseUserManager()
    basket_window = BasketWindow(user_id=100,
                                 database_user_manager=database_user_manager,
                                 database_product_manager=database_product_manager,
                                 basket={0: 1, 2: 2, 7: 1})
    basket_window.show()
    sys.exit(app.exec())
