import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QApplication


class InfoWindow(QWidget):
    """Информационное окно"""

    def __init__(self, title: str, message: str) -> None:
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(400, 180)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
            }
        """)

        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        # Сообщение
        label: QLabel = QLabel(message)
        label.setFont(QFont("Arial", 12))
        label.setStyleSheet("color: black; background-color: white;")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Кнопка "ОК"
        btn: QPushButton = QPushButton("ОК")
        btn.setFont(QFont("Arial", 12))
        btn.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                color: white;
                background-color: rgb(0, 220, 106);
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(0, 152, 0);
            }
        """)
        btn.clicked.connect(self.close)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)


if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    info_window: InfoWindow = InfoWindow("Успех", "Регистрация прошла успешно!")
    info_window.show()
    sys.exit(app.exec())
