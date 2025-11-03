import sys
from typing import Optional

from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve, Qt
from PyQt6.QtWidgets import (
    QWidget, QApplication, QLabel, QRadioButton, QButtonGroup, QMainWindow
)


class SlidingMenu(QWidget):
    """
    Боковое меню с анимацией выезда и фильтрами сортировки.
    """

    def __init__(self, parent: Optional[QWidget] = None, main_window: Optional[QMainWindow] = None) -> None:
        super().__init__(parent)
        self.main_window: Optional[QMainWindow] = main_window

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(-350, 350, 350, 990)

        # Контейнер с фоном
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 350, 990)
        self.container.setStyleSheet(
            "background-color: #e6deff; border-radius: 10px; border: 6px solid rgb(92, 83, 220);"
        )

        # Прозрачный контент для виджетов
        self.content = QWidget(self)
        self.content.setGeometry(0, 0, 350, 990)
        self.content.setStyleSheet("background-color: transparent;")

        # Заголовок фильтров
        label_filters = QLabel("Фильтры", self.content)
        label_filters.setGeometry(100, 25, 150, 30)
        label_filters.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_filters.setStyleSheet("font-size: 26px; font-family: 'Arial';")

        # Подзаголовок сортировки
        label_filter = QLabel("Сортировать по:", self.content)
        label_filter.setGeometry(13, 70, 150, 30)
        label_filter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_filter.setStyleSheet("font-size: 20px; font-family: 'Arial';")

        # Радиокнопки сортировки
        self.radio1 = QRadioButton("Цене убывание", self.content)
        self.radio1.setGeometry(13, 110, 150, 30)
        self.radio1.setStyleSheet("font-size: 16px; font-family: 'Arial';")

        self.radio2 = QRadioButton("Цене возрастание", self.content)
        self.radio2.setGeometry(13, 145, 200, 30)
        self.radio2.setStyleSheet("font-size: 16px; font-family: 'Arial';")

        self.radio3 = QRadioButton("По названию", self.content)
        self.radio3.setGeometry(13, 180, 150, 30)
        self.radio3.setStyleSheet("font-size: 16px; font-family: 'Arial';")

        # Группировка радиокнопок
        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.radio1)
        self.radio_group.addButton(self.radio2)
        self.radio_group.addButton(self.radio3)

        # Анимация
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def slide_in(self) -> None:
        """Показать меню с анимацией."""
        start_rect = self.geometry()
        end_rect = QRect(0, 0, 350, 990)
        self.animate(start_rect, end_rect)

    def slide_out(self) -> None:
        """Скрыть меню с анимацией."""
        start_rect = self.geometry()
        end_rect = QRect(-350, 350, 350, 990)
        self.animate(start_rect, end_rect)

    def animate(self, start_rect: QRect, end_rect: QRect) -> None:
        """Запустить анимацию изменения геометрии."""
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()


class TestMainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Тест бокового меню")
        self.setGeometry(100, 100, 800, 600)

    def switch_to_worker_menu(self) -> None:
        print("Переход в меню товаров (Worker)")

    def switch_of_for_admin(self) -> None:
        print("Переход в меню администратора (Admin)")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    test_main_window = TestMainWindow()
    test_main_window.show()

    sliding_menu = SlidingMenu(parent=test_main_window, main_window=test_main_window)
    sliding_menu.show()
    sliding_menu.slide_in()

    sys.exit(app.exec())
