from datetime import datetime
import pandas as pd
from database.get_abs_path import get_abs_path
from utils import InvalidCsvOrdersError


class DataBaseOrdersManager:
    """Менеджер работы с заказами в CSV"""

    def __init__(self) -> None:
        self.orders: pd.DataFrame = pd.DataFrame()
        self.file_path: str = get_abs_path('system_file', 'orders.csv')
        self.__read_orders()
        # print(self.orders)
        # print(self.orders.info())

    def __read_orders(self) -> None:
        """Чтение заказов из CSV"""
        try:
            self.orders = pd.read_csv(
                self.file_path,
                encoding='UTF-8',
                dtype={"id_product":int, "user_id": int, "quantity": int, 'address': str},
                parse_dates=["purchase_datetime"]
            )
        except Exception as e:
            print(InvalidCsvOrdersError(str(e)))

    def get_orders(self) -> pd.DataFrame:
        """Получение всех заказов"""
        return self.orders

    def get_orders_by_id(self, product_id: int) -> pd.DataFrame:
        return self.orders.loc[self.orders['user_id'] == product_id]

    def write_row(self, product_id: int, user_id: int, quantity: int, address: str) -> None:
        """Добавление нового заказа"""
        now: datetime = datetime.now()
        formatted_date: str = now.strftime("%Y-%m-%d %H:%M:%S")
        self.orders.loc[len(self.orders)] = {
            'id_product': product_id,
            'user_id': user_id,
            'purchase_datetime': formatted_date,
            'quantity': quantity,
            'address': address
        }

    def save(self) -> None:
        """Сохраняет все изменения в CSV"""
        self.orders.to_csv(
            self.file_path,
            index=False,
            encoding='UTF-8'
        )


if __name__ == "__main__":
    database_product_manager: DataBaseOrdersManager = DataBaseOrdersManager()
    # database_product_manager.write_row(
    #     product_id=1,
    #     user_id=100,
    #     quantity=1,
    #     address=" ")
    # print(database_product_manager.get_orders_by_id(100))
    # database_product_manager.save()
