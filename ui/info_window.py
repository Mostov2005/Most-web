from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout


class InfoWindow(QWidget):
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)

        btn = QPushButton("Ок")
        btn.clicked.connect(self.close)
        layout.addWidget(btn)

        self.setLayout(layout)
