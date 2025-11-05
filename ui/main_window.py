import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi

import qt_env  # noqa: F401
from core.recommender import Recommender
from database import DataBaseUserManager, DataBaseProductManager, get_abs_path
from ui.admin_window import AdminWindow
from ui.balance_window import AddBalance
from ui.basket_window import BasketWindow
from ui.worker_window import WorkerWindow
from widgets.product_table import ProductTable
from widgets.sliding_menu import SlidingMenu


class MainWindow(QMainWindow):
    """Главное окно """

    def __init__(self, database_user_manager: DataBaseUserManager, database_product_manager: DataBaseProductManager,
                 user_id: int, type_avt: str) -> None:
        super().__init__()
        ui_path = get_abs_path('system_file', 'main_window.ui')
        loadUi(ui_path, self)
        self.move(0, 0)

        self.user_id: int = user_id
        self.basket: dict[int, int] = {}
        self.type_avt: str = type_avt

        self.database_user_manager: DataBaseUserManager = database_user_manager
        self.database_product_manager: DataBaseProductManager = database_product_manager
        self.recommender: Recommender = Recommender(self.database_product_manager)
        self.product_table: ProductTable = ProductTable(self.tableWidget)
        self.menu: SlidingMenu = SlidingMenu(self, self)

        self.product_table.add_product_in_basket_signal.connect(self.add_product_in_basket)
        self.poisk_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_admin.clicked.connect(self.switch_of_for_admin)
        self.button_worker.clicked.connect(self.switch_to_worker_menu)
        self.toggle_btn.clicked.connect(self.toggle_menu)
        self.popolnenie_balans_btn.clicked.connect(self.switch_to_balans_window)
        self.basket_btn.clicked.connect(self.switch_to_basket)

        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)

        self.show_button()
        self.update_table()
        self.update_balance_button()
        self.update_name_label()

    def show_button(self) -> None:
        """Скрывает кнопки, недоступные для текущей роли"""
        if self.type_avt == 'Buyer':
            self.button_admin.hide()
            self.button_worker.hide()
        elif self.type_avt == 'Worker':
            self.button_admin.hide()

    def toggle_menu(self) -> None:
        """Открывает или закрывает боковое меню"""
        if self.menu.geometry().x() < 0:
            self.menu.slide_in()
        else:
            self.menu.slide_out()

    def update_table(self) -> None:
        """Обновляет таблицу продуктов с учетом рекомендаций"""
        products_id = self.recommender.get_recommendation_products_id()
        products = self.database_product_manager.get_products_by_id(products_id)
        self.product_table.update_table(products)

    def add_product_in_basket(self, product_id: int) -> None:
        """Добавляет продукт в корзину"""
        self.basket[product_id] = self.basket.get(product_id, 0) + 1
        self.update_count_product()

    def update_count_product(self) -> None:
        """Обновляет отображение количества товаров в корзине"""
        count_product = sum(self.basket.values())
        self.basket_btn.setText(f'🛒 Корзина: {count_product}')

    def update_name_label(self) -> None:
        """Обновляет отображение имени пользователя"""
        name = self.database_user_manager.get_name_by_id(self.user_id)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setText(name)

    def switch_of_for_admin(self) -> None:
        """Переход в окно администратора"""
        self.for_admin_window: AdminWindow = AdminWindow(self.database_user_manager, self.user_id)
        self.for_admin_window.back_signal.connect(self.show)
        self.for_admin_window.show()
        self.hide()

    def switch_to_worker_menu(self) -> None:
        """Переход в окно работника"""
        self.for_workers_window: WorkerWindow = WorkerWindow(self.database_product_manager)
        self.for_workers_window.back_signal.connect(lambda: (self.show(), self.update_table()))
        self.for_workers_window.show()
        self.hide()

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

    def close_basket_window(self, basket: dict[int, int]) -> None:
        """Обновляет корзину после закрытия окна корзины"""
        self.basket = basket.copy()
        self.show()
        self.update_balance_button()
        self.update_count_product()

    def switch_to_basket(self) -> None:
        """Переход в окно корзины"""
        self.basket_window: BasketWindow = BasketWindow(self.user_id,
                                                        self.database_user_manager,
                                                        self.database_product_manager,
                                                        self.basket)
        self.basket_window.basket_updated.connect(self.close_basket_window)
        self.hide()
        self.basket_window.show()


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    database_user_manager: DataBaseUserManager = DataBaseUserManager()
    database_product_manager: DataBaseProductManager = DataBaseProductManager()

    main_window: MainWindow = MainWindow(database_user_manager, database_product_manager, 100, 'Admin')
    main_window.show()
    sys.exit(app.exec())
