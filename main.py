import sys
from typing import Any

from PyQt6.QtWidgets import QApplication

import qt_env  # noqa: F401
from database import DataBaseUserManager, DataBaseProductManager, DataBaseOrdersManager
from ui import WelcomeWindow, MainWindow


class MostWeb:
    """
    Главный класс приложения, который управляет всеми окнами
    """

    def __init__(self) -> None:
        # Менеджеры работы с базой данных
        self.database_user_manager: DataBaseUserManager = DataBaseUserManager()
        self.database_product_manager: DataBaseProductManager = DataBaseProductManager()
        self.database_orders_manager: DataBaseOrdersManager = DataBaseOrdersManager()

        # Окно приветствия
        self.welcome_window: WelcomeWindow = WelcomeWindow(self.database_user_manager)
        self.welcome_window.valid_user_signal.connect(self.handle_window_signal)
        self.welcome_window.show()

    def handle_window_signal(self, id_user: int, type_avt: Any) -> None:
        """
        Обработка сигнала успешной авторизации пользователя из WelcomeWindow.

        :param id_user: ID авторизованного пользователя
        :param type_avt: Тип аккаунта пользователя (например, роль)
        """
        self.welcome_window.close()
        main_window: MainWindow = MainWindow(
            self.database_user_manager,
            self.database_product_manager,
            self.database_orders_manager,
            id_user,
            type_avt
        )
        main_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    most_web = MostWeb()
    sys.exit(app.exec())
