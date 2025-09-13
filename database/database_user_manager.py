import pandas as pd
import os
import csv
from utils import InvalidCSVError, InvalidAddUserError
from core import PasswordHasher


class DataBaseUserManager:
    def __init__(self):
        self.users = pd.DataFrame()
        self.ph = PasswordHasher
        self.file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'system_file', 'users.csv')
        )
        self.__read_users()

    def __read_users(self):
        try:
            self.users = pd.read_csv(self.file_path, encoding='UTF-8', index_col="id")
        except Exception as e:
            print(InvalidCSVError(str(e)))

    def __get_max_id(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                ids = [int(row["id"]) for row in reader]
                max_id = max(ids) if ids else 0
        except FileNotFoundError:
            max_id = 0
        return max_id

    def get_users(self):
        return self.users

    def check_valid_users(self, name, password):
        row = self.users.loc[self.users["name"] == name]
        if row.empty:
            return None
        if self.ph.hash_password(password) == row.iloc[0]["hash"]:
            return int(row.iloc[0]['id']), row['role']
        return None

    def check_user_availability(self, login):
        return not self.users.loc[self.users["name"] == login].empty

    def check_email_availability(self, email):
        return not self.users.loc[self.users["email"] == email].empty

    def check_phone_availability(self, phone):
        cleaned_phone = phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
        return not self.users.loc[self.users["phone"] == cleaned_phone].empty

    def add_new_user(self, login: str, email: str, phone: str, password: str):
        cleaned_phone = (phone.replace("(", "")
                         .replace(")", "")
                         .replace("-", "")
                         .replace(" ", ""))
        hash_password = self.ph.hash_password(password)

        # Данные для записи
        new_id = self.__get_max_id() + 1
        try:
            self.users.loc[len(self.users)] = {
                'id': new_id,
                'name': login,
                'hash': hash_password,
                'email': email,
                'phone': cleaned_phone,
                'role': 'buyer',
                'balance': 0
            }

            self.users.to_csv(self.file_path, index=False, encoding='UTF-8')
        except Exception as e:
            print(InvalidAddUserError(str(e)))

    def get_user_by_id(self, user_id):
        return self.users.loc[user_id]


if __name__ == "__main__":
    database_manager = DataBaseUserManager()
    print(database_manager.check_user_availability('32133'))
    print(database_manager.get_user_by_id(0))

    # database_manager.add_new_user("1", "1", "1", "1")
