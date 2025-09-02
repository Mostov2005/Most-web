import json
import sys
import re
import os
import shutil

from PyQt6.QtCore import pyqtSignal, QPropertyAnimation, QRect, QEasingCurve, Qt, QRegularExpression
from PyQt6.QtGui import QPixmap, QIntValidator, QFont, QRegularExpressionValidator
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QRadioButton, QButtonGroup, QComboBox, QFileDialog
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QVBoxLayout, QMainWindow, QMessageBox, QLineEdit

from core import PasswordHasher


# Боковое меню(Подраздел главного окна)
class SlidingMenu(QWidget):
    def __init__(self, parent=None, main_window=None):
        super(SlidingMenu, self).__init__(parent)
        self.main_window = main_window  # Store the reference to MainWindow

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(-350, 350, 350, 990)  # Initial position off-screen

        # Create a container widget for border
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 350, 990)
        self.container.setStyleSheet(
            "background-color: #e6deff; border-radius: 10px; border: 6px solid rgb(92, 83, 220);"
        )

        # Create the main widget for control elements
        self.content = QWidget(self)
        self.content.setGeometry(0, 0, 350, 990)
        self.content.setStyleSheet("background-color: transparent;")  # Transparent background

        # Add text "Фильтры"
        label_filters = QLabel("Фильтры", self.content)
        label_filters.setGeometry(100, 25, 150, 30)
        label_filters.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_filters.setStyleSheet("font-size: 26px; font-family: 'Arial';")

        label_filter = QLabel("Сортировать по:", self.content)
        label_filter.setGeometry(13, 70, 150, 30)
        label_filter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_filter.setStyleSheet("font-size: 20px; font-family: 'Arial';")

        # Add radio buttons for filters
        radio1 = QRadioButton("Цене убывание", self.content)
        radio1.setGeometry(13, 110, 150, 30)
        radio1.setStyleSheet("font-size: 16px; font-family: 'Arial';")

        radio2 = QRadioButton("Цене возрастание", self.content)
        radio2.setGeometry(13, 145, 200, 30)
        radio2.setStyleSheet("font-size: 16px; font-family: 'Arial';")

        radio3 = QRadioButton("По названию", self.content)
        radio3.setGeometry(13, 180, 150, 30)
        radio3.setStyleSheet("font-size: 16px; font-family: 'Arial';")

        radio_group = QButtonGroup(self)
        radio_group.addButton(radio1)
        radio_group.addButton(radio2)
        radio_group.addButton(radio3)

        self.label_worker = QLabel("Для работников", self.content)
        self.label_worker.setStyleSheet("font-size: 20px; font-family: 'Arial';")
        self.label_worker.setGeometry(100, 300, 150, 30)
        self.label_worker.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add button for worker
        self.button_worker = QPushButton("Меню товаров", self.content)
        self.button_worker.setGeometry(50, 350, 250, 40)
        self.button_worker.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                color: white;
                background-color: rgb(0, 0, 255);
                font-size: 16px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: rgb(0, 0, 158);
            }
        """)
        self.button_worker.clicked.connect(self.main_window.switch_to_worker_menu)

        # Add text "Для администратора"
        self.label_admin = QLabel("Для администраторов", self.content)
        self.label_admin.setGeometry(77, 500, 204, 30)  # Set coordinates and sizes
        self.label_admin.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center alignment
        self.label_admin.setStyleSheet("font-size: 20px; font-family: 'Arial';")  # Set font size

        # Add button for administrator
        self.button_admin = QPushButton("Меню администратора", self.content)
        self.button_admin.setGeometry(50, 550, 250, 40)  # Set coordinates and sizes
        self.button_admin.clicked.connect(self.main_window.switch_of_for_admin)
        self.button_admin.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                color: white;
                background-color: rgb(0, 0, 255);
                font-size: 16px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: rgb(0, 0, 158);
            }
        """)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)  # Reduce animation duration
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)  # Smooth animation

    def slide_in(self):
        start_rect = self.geometry()
        end_rect = QRect(0, 0, 350, 990)
        self.animate(start_rect, end_rect)

    def slide_out(self):
        start_rect = self.geometry()
        end_rect = QRect(-350, 350, 350, 990)
        self.animate(start_rect, end_rect)

    def animate(self, start_rect, end_rect):
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()

    def hide_btn(self, status):
        if status == 'Buyer':
            self.label_admin.hide()
            self.button_admin.hide()
            self.label_worker.hide()
            self.button_worker.hide()
        elif status == 'Worker':
            self.label_admin.hide()
            self.button_admin.hide()
