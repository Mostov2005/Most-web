class InvalidCSVError(Exception):
    def __init__(self, message=""):
        self.start_message = "Не удалось считать пользователей: "
        self.message = self.start_message + message
        super().__init__(self.message)


class InvalidAddUserError(Exception):
    def __init__(self, message=""):
        self.start_message = "Не удалось добавить пользователя: "
        self.message = self.start_message + message
        super().__init__(self.message)


class InvalidJsonError(Exception):
    def __init__(self, message=""):
        self.start_message = "Не удалось считать товары: "
        self.message = self.start_message + message
        super().__init__(self.message)
