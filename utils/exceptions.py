class InvalidCsvUserError(Exception):
    def __init__(self, message=""):
        self.start_message = "Не удалось считать пользователей: "
        self.message = self.start_message + message
        super().__init__(self.message)


class InvalidAddUserError(Exception):
    def __init__(self, message=""):
        self.start_message = "Не удалось добавить пользователя: "
        self.message = self.start_message + message
        super().__init__(self.message)


class InvalidAddProductError(Exception):
    def __init__(self, message=""):
        self.start_message = "Не удалось добавить товар: "
        self.message = self.start_message + message
        super().__init__(self.message)


class InvalidCsvProductError(Exception):
    def __init__(self, message=""):
        self.start_message = "Не удалось считать товары: "
        self.message = self.start_message + message
        super().__init__(self.message)


class InvalidCsvOrdersError(Exception):
    def __init__(self, message=""):
        self.start_message = "Не удалось считать историю покупок: "
        self.message = self.start_message + message
        super().__init__(self.message)
