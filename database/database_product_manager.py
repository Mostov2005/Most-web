import pandas as pd
import os
import json
from utils import InvalidJsonError
from core import PasswordHasher


class DataBaseProductManager:
    def __init__(self):
        self.products = pd.DataFrame()
        self.ph = PasswordHasher
        self.file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'system_file', 'products.csv')
        )
        self.__read_products()

    def __read_products(self):
        try:
            self.products = pd.read_csv(self.file_path, encoding='UTF-8', index_col="id")
        except Exception as e:
            print(InvalidJsonError(str(e)))

    def get_products(self):
        return self.products

    def get_product_by_id(self, id_product):
        return self.products.loc[id_product]

    def get_products_by_id(self, products_id: list) -> list:
        products = []
        for id_product in products_id:
            products.append(self.get_product_by_id(id_product))
        return products


if __name__ == "__main__":
    database_product_manager = DataBaseProductManager()
    print(database_product_manager.get_product_by_id(20))
