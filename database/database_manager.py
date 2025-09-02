import pandas as pd
import os
from utils import InvalidCSVError
from core import PasswordHasher


class DataBaseManager:
    def __init__(self):
        self.users = pd.DataFrame()
        self.ph = PasswordHasher
        self.__read_users()

    def __read_users(self):
        try:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'system_file', 'users.csv')
            file_path = os.path.abspath(file_path)
            self.users = pd.read_csv(file_path, encoding='UTF-8')
        except Exception as e:
            print(InvalidCSVError(str(e)))

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
        row = self.users.loc[self.users["name"] == login]
        if row:
            return True
