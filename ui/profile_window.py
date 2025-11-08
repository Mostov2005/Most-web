import sys
from datetime import datetime

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem
from PyQt6.uic import loadUi

import qt_env  # noqa: F401
from database import DataBaseUserManager, DataBaseProductManager, get_abs_path, DataBaseOrdersManager
from ui.balance_window import AddBalance


class ProfileWindow(QMainWindow):
    """Окно пользователя """
    back_signal = pyqtSignal()

    def __init__(self, database_user_manager: DataBaseUserManager,
                 database_product_manager: DataBaseProductManager,
                 database_orders_manager: DataBaseOrdersManager,
                 user_id: int) -> None:
        super().__init__()
        ui_path = get_abs_path('system_file', 'profile_window.ui')
        loadUi(ui_path, self)
        self.move(0, 0)

        self.user_id: int = user_id

        self.database_user_manager: DataBaseUserManager = database_user_manager
        self.database_product_manager: DataBaseProductManager = database_product_manager
        self.database_orders_manager: DataBaseOrdersManager = database_orders_manager

        self.popolnenie_balans_btn.clicked.connect(self.switch_to_balans_window)
        self.back_menu_btn.clicked.connect(self.switch_of_main)

        self.table_orders.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_orders.setSortingEnabled(True)
        self.table_orders.horizontalHeader().setSortIndicatorShown(True)

        self.update_balance_button()
        self.update_name_label()
        self.update_table()

    def switch_to_balans_window(self) -> None:
        """Переход в окно пополнения баланса"""
        self.plus_balans: AddBalance = AddBalance(self.database_user_manager, self.user_id)
        self.plus_balans.back_signal.connect(self.show)
        self.plus_balans.back_signal.connect(self.update_balance_button)
        self.plus_balans.show()
        self.hide()

    def update_balance_button(self) -> None:
        """Обновляет отображение баланса на кнопке пополнения"""
        balance_user = self.database_user_manager.get_balance_by_id(self.user_id)
        self.popolnenie_balans_btn.setText(f'+ {balance_user}₽')

    def update_name_label(self) -> None:
        """Обновляет отображение имени пользователя"""
        name = self.database_user_manager.get_name_by_id(self.user_id)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setText(name)

    def update_table(self):
        """Обновление таблицы"""
        data = self.database_orders_manager.get_orders_by_id(self.user_id)
        for row_index, product_tuple in enumerate(data.iterrows()):
            self.table_orders.insertRow(row_index)

            product = product_tuple[1]
            index_product: int = product.get('id_product', 0)
            date_product: datetime = product.get('purchase_datetime', datetime.now())
            quantity: int = product.get('quantity', 1)
            address: str = product.get('address', 'Самовывоз').strip()
            if address == '':
                address = 'Самовывоз'

            info_product = self.database_product_manager.get_product_by_id(index_product)
            name_product: str = info_product.get('name', '')
            price_product: int = info_product.get('price', 0)

            # Заполняем каждую ячейку
            self.table_orders.setItem(row_index, 0, QTableWidgetItem(str(date_product)))
            self.table_orders.setItem(row_index, 1, QTableWidgetItem(name_product))
            self.table_orders.setItem(row_index, 2, QTableWidgetItem(f'{str(price_product)} ₽'))
            self.table_orders.setItem(row_index, 3, QTableWidgetItem(f'{str(price_product * quantity)} ₽'))
            self.table_orders.setItem(row_index, 4, QTableWidgetItem(str(quantity)))
            self.table_orders.setItem(row_index, 5, QTableWidgetItem(address))

    def switch_of_main(self) -> None:
        """Возврат в главное меню"""
        self.back_signal.emit()
        self.close()


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    database_user_manager: DataBaseUserManager = DataBaseUserManager()
    database_product_manager: DataBaseProductManager = DataBaseProductManager()
    database_orders_manager: DataBaseOrdersManager = DataBaseOrdersManager()

    profile_window: ProfileWindow = ProfileWindow(database_user_manager, database_product_manager,
                                                  database_orders_manager, 100)
    profile_window.show()
    sys.exit(app.exec())
