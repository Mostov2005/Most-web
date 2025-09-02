import re


def validate_login(text):
    if len(text) < 5:
        return 'Логин должен состоять не менее чем из 5 символов'
    elif re.search(r'[^a-zA-Z0-9]', text):
        return 'В логине могут использоваться только буквы латинского алфавита и цифры'
    return None


def validate_email(self, text):
    self.flag_email = False
    self.error_email_label.clear()
    self.error_registration_label.clear()
    if not self.email_edit.hasAcceptableInput():
        self.error_email_label.setText("Введен некорректный email")
    for user in users.values():
        if self.email_edit.text() == user[2]:
            self.error_email_label.setText('Пользователь с таким email уже существует')
    else:
        self.flag_email = True


def validate_phone(self, text):
    self.flag_phone = False
    self.error_phone_label.clear()
    self.error_registration_label.clear()
    if len(text) < 18:
        self.error_phone_label.setText('Неверно введен номер телефона')
    for user in users.values():
        if self.phone_edit.text() == user[3]:
            self.error_phone_label.setText('Пользователь с таким номером телефона уже существует')
    else:
        self.flag_phone = True


def validate_password(self, text):
    self.flag_paroll = False
    self.error_parol_label.clear()
    self.error_registration_label.clear()
    if len(text) < 8:
        self.error_parol_label.setText('Пароль должен состоять не менее чем из 8 символов')

    elif not re.search('[a-z]', text):
        self.error_parol_label.setText(
            'Пароль должен содержать как минимум одну строчную букву латинского алфавита')

    elif not re.search('[A-Z]', text):
        self.error_parol_label.setText(
            'Пароль должен содержать как минимум одну прописную букву латинского алфавита')

    elif not re.search('[0-9]', text):
        self.error_parol_label.setText('Пароль должен содержать хотя бы одну цифру')

    elif not re.search('[!@#$%^&*(),.?":{}|<>_-]', text):
        self.error_parol_label.setText('Пароль должен содержать хотя бы один специальный символ')

    else:
        self.flag_paroll = True


def validate_password_repeat(self, text):
    self.flag_return_paroll = False
    self.error_return_paroll_label.clear()
    self.error_registration_label.clear()
    if text != self.paroll_edit.text():
        self.error_return_paroll_label.setText('Пароли не совпадают')
    else:
        self.flag_return_paroll = True


def validate_regist(self):
    self.error_registration_label.clear()
    if not (all([self.flag_login, self.flag_email, self.flag_phone, self.flag_paroll, self.flag_return_paroll])):
        self.error_registration_label.setText('Заполните все поля для регистрации')

    else:
        login = (self.login_edit.text())
        email = (self.email_edit.text())
        phone = (self.phone_edit.text())
        status = 'Buyer'
        balans = 0
        password = PasswordHasher().hash_password(self.paroll_edit.text())
        polzovael = []
        polzovael.append(login), polzovael.append(password), polzovael.append(email), polzovael.append(
            phone), polzovael.append(status), polzovael.append(balans)

        print(polzovael)
        users[login] = polzovael
        with open('system_file\\users.csv', 'w') as file:
            json.dump(users, file, ensure_ascii=False, indent=2)

        self.switch_on_welcome()
