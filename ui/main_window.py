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


# Главное окно
class MainWindow(QMainWindow):
    def __init__(self, database_user_manager, database_product_manager, user_id):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'system_file', 'main_window.ui')
        ui_path = os.path.abspath(ui_path)
        loadUi(ui_path, self)

        self.database_user_manager = database_user_manager
        self.database_product_manager = database_product_manager
        self.recommender = Recommender(self.database_product_manager)
        self.product_table = ProductTable(self.tableWidget)
        self.product_table.add_product_in_basket_signal.connect(self.add_product_in_basket)

        self.user_id = user_id

        # self.setWindowState(Qt.WindowFullScreen)
        self.move(0, 0)

        self.user_id = user_id

        self.menu = SlidingMenu(self, self)

        self.toggle_btn.clicked.connect(self.toggle_menu)
        self.poisk_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.basket_btn.clicked.connect(self.switch_to_basket)
        # self.popolnenie_balans_btn.clicked.connect(self.switch_to_plus_balance)

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
        products_id = self.recommender.get_recommendation_products_id()
        products = self.database_product_manager.get_products_by_id(products_id)

        self.product_table.update_table(products)

    def add_product_in_basket(self, product_id):
        print(product_id)

        # def switch_of_for_admin(self):
    #     self.for_admin_window = SetingForAdmin(self.name)
    #     self.close()
    #     self.for_admin_window.show()
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
    # def update_balance_label(self, name):
    #     self.name = name
    #     self.name_label.setText(self.name)
    #     self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     self.popolnenie_balans_btn.setText(f'+ {users[self.name][5]}₽')
    #     self.status = users[self.name][4]
    #     self.menu.hide_btn(self.status)
    #     self.update_basket_label()

    # def switch_to_basket(self):
    #     self.basket_window = Oformalenie_Zakaza(self.name)
    #     self.basket_window.basket_updated.connect(self.update_basket_label)
    #     self.close()
    #     self.basket_window.show()
    #
    # def switch_to_plus_balance(self):
    #     self.plus_balans = Poplnenie_balansa(self.name)
    #     self.plus_balans.balance_updated.connect(self.update_balance_label)
    #     self.close()
    #     self.plus_balans.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_user_manager = DataBaseUserManager()
    database_product_manager = DataBaseProductManager()

    main_window = MainWindow(database_user_manager, database_product_manager, 0)
    main_window.show()
    sys.exit(app.exec())

# ("font-size: 20px; font-family: 'Arial';")
