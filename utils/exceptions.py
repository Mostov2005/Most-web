class InvalidCsvUserError(Exception):
    def __init__(self, message: str = "") -> None:
        self.start_message: str = "Не удалось считать пользователей: "
        self.message: str = self.start_message + message
        super().__init__(self.message)


class InvalidAddUserError(Exception):
    def __init__(self, message: str = "") -> None:
        self.start_message: str = "Не удалось добавить пользователя: "
        self.message: str = self.start_message + message
        super().__init__(self.message)


class InvalidAddProductError(Exception):
    def __init__(self, message: str = "") -> None:
        self.start_message: str = "Не удалось добавить товар: "
        self.message: str = self.start_message + message
        super().__init__(self.message)


class InvalidCsvProductError(Exception):
    def __init__(self, message: str = "") -> None:
        self.start_message: str = "Не удалось считать товары: "
        self.message: str = self.start_message + message
        super().__init__(self.message)


class InvalidCsvOrdersError(Exception):
    def __init__(self, message: str = "") -> None:
        self.start_message: str = "Не удалось считать историю покупок: "
        self.message: str = self.start_message + message
        super().__init__(self.message)
