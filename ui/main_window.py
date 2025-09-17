import sys
import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi

from database import DataBaseUserManager
from database import DataBaseProductManager
from widgets.sliding_menu import SlidingMenu
from widgets.product_table import ProductTable
from core.recommender import Recommender
from ui.admin_window import AdminWindow
from ui.balance_window import AddBalance


# Главное окно
class MainWindow(QMainWindow):
    def __init__(self, database_user_manager, database_product_manager, user_id):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'system_file', 'main_window.ui')
        ui_path = os.path.abspath(ui_path)
        loadUi(ui_path, self)
        self.move(0, 0)
        # self.setWindowState(Qt.WindowFullScreen)
        self.user_id = user_id

        self.database_user_manager = database_user_manager
        self.database_product_manager = database_product_manager
        self.recommender = Recommender(self.database_product_manager)
        self.product_table = ProductTable(self.tableWidget)
        self.menu = SlidingMenu(self, self)

        self.product_table.add_product_in_basket_signal.connect(self.add_product_in_basket)
        self.poisk_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_admin.clicked.connect(self.switch_of_for_admin)
        self.toggle_btn.clicked.connect(self.toggle_menu)
        self.popolnenie_balans_btn.clicked.connect(self.switch_to_balans_window)
        # self.basket_btn.clicked.connect(self.switch_to_basket)

        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)

        self.update_table()
        self.update_balance_button()
        self.update_name_label()

        # self.update_balance_label()

    def toggle_menu(self):
        if self.menu.geometry().x() < 0:
            self.menu.slide_in()
        else:
            self.menu.slide_out()

    def update_table(self):
        products_id = self.recommender.get_recommendation_products_id()
        products = self.database_product_manager.get_products_by_id(products_id)

        self.product_table.update_table(products)

    def add_product_in_basket(self, product_id):
        print(product_id)

    def update_name_label(self):
        name = self.database_user_manager.get_name_by_id(self.user_id)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setText(name)

    def switch_of_for_admin(self):
        self.for_admin_window = AdminWindow(self.database_user_manager, self.user_id)

        # Когда админское окно закроется через сигнал -> показать главное
        self.for_admin_window.back_signal.connect(self.show)

        self.for_admin_window.show()
        self.hide()

    def switch_to_balans_window(self):
        self.plus_balans = AddBalance(self.database_user_manager, self.user_id)
        self.plus_balans.back_signal.connect(self.show)
        self.plus_balans.back_signal.connect(self.update_balance_button)
        self.plus_balans.show()

        self.hide()

    def update_balance_button(self):
        balance_user = self.database_user_manager.get_balance_by_id(self.user_id)
        self.popolnenie_balans_btn.setText(f'+ {balance_user}₽')

    #
    # def switch_to_worker_menu(self):
    #     self.for_workers_window = SetingForWorkers()
    #     self.for_workers_window.table_updated.connect(self.update_table)
    #     self.close()
    #     self.for_workers_window.show()

    # def update_basket_label(self):
    #     self.count_tovar_label.setText(f'{len(basket)}: {summ_basket} ₽')
    #     self.count_tovar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     self.popolnenie_balans_btn.setText(f'+ {users[self.name][5]}₽')
    #

    # def switch_to_basket(self):
    #     self.basket_window = Oformalenie_Zakaza(self.name)
    #     self.basket_window.basket_updated.connect(self.update_basket_label)
    #     self.close()
    #     self.basket_window.show()
    #


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_user_manager = DataBaseUserManager()
    database_product_manager = DataBaseProductManager()

    main_window = MainWindow(database_user_manager, database_product_manager, 100)
    main_window.show()
    sys.exit(app.exec())

# ("font-size: 20px; font-family: 'Arial';")
