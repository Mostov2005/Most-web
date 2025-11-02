import pandas as pd
import os
from utils import InvalidCsvOrdersError
from database.get_abs_path import get_abs_path
from datetime import datetime


class DataBaseOrdersManager:
    def __init__(self):
        self.orders = pd.DataFrame()
        self.file_path = get_abs_path('system_file', 'orders.csv')
        self.__read_orders()
        # print(self.orders)
        # print(self.orders.info())

    def __read_orders(self):
        try:
            self.orders = pd.read_csv(
                self.file_path,
                encoding='UTF-8',
                index_col="id_product",
                dtype={"user_id": int, "quantity": int},
                parse_dates=["purchase_datetime"]
            )
        except Exception as e:
            print(InvalidCsvOrdersError(str(e)))

    def get_orders(self):
        return self.orders

    def write_row(self, product_id, user_id, quantity):
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        self.orders.loc[len(self.orders)] = {
            'id_product': product_id,
            'user_id': user_id,
            'purchase_datetime': formatted_date,
            'quantity': quantity}

    def save(self):
        """Сохраняет все изменения в CSV."""
        self.orders.to_csv(self.file_path, index=True, index_label="id_product", encoding='UTF-8')


if __name__ == "__main__":
    database_product_manager = DataBaseOrdersManager()
