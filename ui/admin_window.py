import sys
import os

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6.QtWidgets import QTableWidgetItem, QComboBox
from PyQt6.uic import loadUi
from database import DataBaseUserManager
from widgets.unsaved_changes_helper import UnsavedChangesHelper


# Для администраторов
class AdminWindow(QMainWindow):
    back_signal = pyqtSignal()

    FONT_SIZE = 12
    ROLE_OPTIONS = ["Buyer", "Worker", "Admin"]
    TABLE_COLUMNS = [50, 200, 250, 250, 150, 150]

    def __init__(self, database_user_manager, user_id):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), '..', 'system_file', 'for_admin.ui')
        ui_path = os.path.abspath(ui_path)
        loadUi(ui_path, self)

        self.move(0, 0)

        self.database_user_manager = database_user_manager
        self.user_id = user_id

        self.font = QFont()
        self.font.setPointSize(self.FONT_SIZE)

        self.delete_btn.clicked.connect(self.delete_user)
        self.save_btn.clicked.connect(self.save_edits)
        self.back_menu_btn.clicked.connect(self.switch_of_main)

        # Настройка таблиц
        self._setup_table(self.table_tec, self.TABLE_COLUMNS)
        self._setup_table(self.table, self.TABLE_COLUMNS)

        self.is_dirty = False  # флаг изменений
        self.populate_table()
        self.table.itemChanged.connect(self._on_item_changed)

    def _on_item_changed(self, item):
        """Ставим флаг, если данные изменились."""
        self.is_dirty = True

    def _setup_table(self, table, column_widths: list[int]) -> None:
        """Устанавливает ширину столбцов таблицы."""
        for col, width in enumerate(column_widths):
            table.setColumnWidth(col, width)

    def populate_table(self) -> None:
        """Загружает всех пользователей и выделяет текущего в отдельной таблице."""
        users = self.database_user_manager.get_users()

        # Очищаем таблицы
        self.table.setRowCount(0)
        self.table_tec.setRowCount(0)

        for user_id, row in users.iterrows():
            values = row.values.tolist()
            if user_id == self.user_id:
                self.table_tec.insertRow(0)
                self._populate_table_tec_row(0, [user_id] + values)
            else:
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                self._populate_row(row_idx, [user_id] + values)

    def _populate_row(self, row: int, user_data: list) -> None:
        """Добавляет одну строку с данными пользователя."""
        for col, value in enumerate(user_data):
            if col == 5:  # Роль
                widget = QComboBox()
                widget.addItems(self.ROLE_OPTIONS)
                widget.setCurrentText(str(value).strip())
                widget.setFont(self.font)
                widget.setStyleSheet("border: none;")
                self.table.setCellWidget(row, col, widget)

            elif col == 6:  # Числовое поле
                widget = QLineEdit()
                widget.setValidator(QIntValidator())
                widget.setText(str(value))
                widget.setFont(self.font)
                widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setCellWidget(row, col, widget)

            else:  # Обычное текстовое поле
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 2 or col == 0:  # Колонка недоступна для редактирования
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)

    def _populate_table_tec_row(self, row: int, user_data: list) -> None:
        """Заполняет строку таблицы текущего пользователя (все поля readonly)."""
        for col, value in enumerate(user_data):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            # Всё делаем нередактируемым
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table_tec.setItem(row, col, item)

    def delete_user(self):
        """Удаляет выбранного пользователя через менеджер и обновляет таблицы."""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите пользователя для удаления.")
            return

        selected_row = selected_items[0].row()
        user_id = self.table.item(selected_row, 0).text()
        username = self.table.item(selected_row, 1).text()

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить пользователя {username}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if reply == QMessageBox.StandardButton.Yes:
                    self.table.removeRow(selected_row)
                    self.database_user_manager.delete_user(int(user_id))
                    self.is_dirty = True
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить пользователя: {e}")

    def save_edits(self):
        """Сохраняет изменения из таблицы в базу данных через менеджер."""

        self.is_dirty = False  # сбрасываем флаг
        for row in range(self.table.rowCount()):
            user_id = int(self.table.item(row, 0).text())  # id всегда readonly
            username = self.table.item(row, 1).text()
            password_hash = self.table.item(row, 2).text()
            email = self.table.item(row, 3).text()
            number = self.table.item(row, 4).text()

            role_combo_box = self.table.cellWidget(row, 5)
            role = role_combo_box.currentText() if role_combo_box else None

            balance_line_edit = self.table.cellWidget(row, 6)
            balance_text = balance_line_edit.text() if balance_line_edit else "0"
            balance = int(balance_text) if balance_text else 0

            # передаём обновлённые данные менеджеру
            self.database_user_manager.update_user(
                user_id=user_id,
                username=username,
                password_hash=password_hash,
                email=email,
                number=number,
                role=role,
                balance=balance
            )

        # в конце сохраняем изменения
        self.database_user_manager.save()

    def switch_of_main(self):
        if self.is_dirty:
            choice = UnsavedChangesHelper.ask_confirmation(self)
            if choice == "yes":
                self.save_edits()
            elif choice == "cancel":
                return

        self.back_signal.emit()
        self.close()

    def closeEvent(self, event):
        if self.is_dirty:
            choice = UnsavedChangesHelper.ask_confirmation(self)
            if choice == "yes":
                self.save_edits()
                event.accept()
            elif choice == "no":
                event.accept()
            else:  # cancel
                event.ignore()
        else:
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    database_user_manager = DataBaseUserManager()

    admin_window = AdminWindow(database_user_manager, 100)
    admin_window.show()
    sys.exit(app.exec())
