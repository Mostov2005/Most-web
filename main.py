import sys
from PyQt6.QtWidgets import QApplication

from core import password_hasher
from database import DataBaseManager
from ui import WelcomeWindow, MainWindow


class MostWeb:
    def __init__(self):
        self.databasemanager = DataBaseManager()

        self.welcome_window = WelcomeWindow(self.databasemanager)
        self.welcome_window.valid_user_signal.connect(self.handle_window_signal)
        self.welcome_window.show()

    def handle_window_signal(self, id, type_avt):
        # Обработка сигнала, который пришел из WelcomeWindow
        print('main')
        self.welcome_window.close()
        print(id, type_avt)
        # self.MainWindow = (self.databasemanager, id, type_avt)
        self.MainWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    most_web = MostWeb()
    sys.exit(app.exec())  # Запуск приложения

# welcome_window.name_updated.connect(main_window.upda te_balance_label)

# try:
#     with open('system_file\\products.json', 'r', encoding='UTF-8') as file:
#         products = json.load(file)
# except json.decoder.JSONDecodeError:
#     products = []
# try:
#     with open('system_file\\users.csv', 'r', encoding='UTF-8') as file:
#         users = json.load(file)
# except json.decoder.JSONDecodeError:
#     users = {}
