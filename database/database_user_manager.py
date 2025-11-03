import csv
import pandas as pd
from core import PasswordHasher
from database.get_abs_path import get_abs_path
from utils import InvalidCsvUserError, InvalidAddUserError


class DataBaseUserManager:
    """Менеджер работы с пользователями в CSV"""

    def __init__(self) -> None:
        self.users: pd.DataFrame = pd.DataFrame()
        self.ph = PasswordHasher
        self.file_path: str = get_abs_path('system_file', 'users.csv')
        self.__read_users()
        # print(self.users)

    def __read_users(self) -> None:
        """Чтение пользователей из CSV"""
        try:
            self.users = pd.read_csv(
                self.file_path,
                encoding='UTF-8',
                index_col="id",
                dtype={"phone": str}
            )
        except Exception as e:
            print(InvalidCsvUserError(str(e)))

    def get_max_id(self) -> int:
        """Получение максимального ID пользователя"""
        max_id: int = self.users.index.max()
        return max_id

    def get_users(self) -> pd.DataFrame:
        """Получение всех пользователей"""
        return self.users

    def check_valid_users(self, name: str, password: str) -> tuple[int, str] | None:
        """Проверка логина и пароля пользователя"""
        row: pd.DataFrame = self.users.loc[self.users["name"] == name]
        if row.empty:
            return None
        if self.ph.hash_password(password) == row.iloc[0]["hash"]:
            user_id: int = int(row.index[0])
            role: str = row.iloc[0]["role"]
            return user_id, role
        return None

    def check_user_availability(self, login: str) -> bool:
        """Проверка существования логина"""
        return not self.users.loc[self.users["name"] == login].empty

    def check_email_availability(self, email: str) -> bool:
        """Проверка существования email"""
        return not self.users.loc[self.users["email"] == email].empty

    def check_phone_availability(self, phone: str) -> bool:
        """Проверка существования номера телефона"""
        cleaned_phone: str = phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        return not self.users.loc[self.users["phone"] == cleaned_phone].empty

    def add_new_user(self, login: str, email: str, phone: str, password: str) -> None:
        """Добавление нового пользователя"""
        cleaned_phone: str = (phone.
                              replace("(", "").
                              replace(")", "").
                              replace("-", "").
                              replace(" ", ""))
        hash_password: str = self.ph.hash_password(password)

        try:
            new_id = self.get_max_id() + 1
            self.users.loc[new_id] = {
                'id': new_id,
                'name': login,
                'hash': hash_password,
                'email': email,
                'phone': cleaned_phone,
                'role': 'Buyer',
                'balance': 0
            }

            self.save()
        except Exception as e:
            print(InvalidAddUserError(str(e)))

    def get_user_by_id(self, user_id: int) -> pd.Series:
        """Получение пользователя по ID"""
        return self.users.loc[user_id]

    def get_balance_by_id(self, user_id: int) -> int:
        """Получение баланса пользователя по ID"""
        row: pd.Series = self.users.loc[user_id]
        return row['balance']

    def get_name_by_id(self, user_id: int) -> str:
        """Получение имени пользователя по ID"""
        row: pd.Series = self.users.loc[user_id]
        return row['name']

    def update_user(
            self,
            user_id: int,
            username: str,
            password_hash: str,
            email: str,
            number: str,
            role: str,
            balance: int
    ) -> None:
        """Обновление данных пользователя"""
        if user_id not in self.users.index:
            raise ValueError(f"Пользователь с id={user_id} не найден")

        self.users.loc[user_id, "name"] = username
        self.users.loc[user_id, "hash"] = password_hash
        self.users.loc[user_id, "email"] = email
        self.users.loc[user_id, "phone"] = str(number)
        self.users.loc[user_id, "role"] = role
        self.users.loc[user_id, "balance"] = balance

    def save(self) -> None:
        """Сохраняет все изменения в CSV"""
        self.users.to_csv(self.file_path, index=True, index_label="id", encoding='UTF-8')

    def delete_user(self, user_id: int) -> None:
        """Удаление пользователя по ID"""
        if user_id not in self.users.index:
            raise ValueError(f"Пользователь с id={user_id} не найден")

        self.users.drop(user_id, inplace=True)

    def set_balance_by_id(self, user_id: int, new_balance: int) -> None:
        """Установка нового баланса пользователю"""
        self.users.loc[user_id, "balance"] = new_balance
        self.save()


if __name__ == "__main__":
    database_manager: DataBaseUserManager = DataBaseUserManager()
    # print(database_manager.check_user_availability('100'))
    # print(database_manager.get_balance_by_id(100))
    database_manager.add_new_user("1", "1", "1", "1")
