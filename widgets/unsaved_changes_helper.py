from PyQt6.QtWidgets import QMessageBox


class UnsavedChangesHelper:
    """Хелпер для проверки несохранённых изменений."""

    @staticmethod
    def ask_confirmation(parent) -> str:
        """
        Показывает диалог и возвращает выбор пользователя:
        "yes", "no", "cancel".
        """
        reply = QMessageBox.question(
            parent,
            "Несохранённые изменения",
            "У вас есть несохранённые изменения. Сохранить перед выходом?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Yes:
            return "yes"
        elif reply == QMessageBox.StandardButton.No:
            return "no"
        else:
            return "cancel"
