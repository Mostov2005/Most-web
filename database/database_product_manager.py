import os
import shutil
import pandas as pd
from database.get_abs_path import get_abs_path
from utils import InvalidCsvProductError, InvalidAddProductError


class DataBaseProductManager:
    """Менеджер работы с продуктами в CSV"""

    def __init__(self) -> None:
        self.products: pd.DataFrame = pd.DataFrame()
        self.file_path: str = get_abs_path('system_file', 'products.csv')
        self.__read_products()
        # print(self.products)
        # print(self.products.info())

    def __read_products(self) -> None:
        """Чтение продуктов из CSV"""
        try:
            self.products = pd.read_csv(self.file_path, encoding='UTF-8', index_col="id")
        except Exception as e:
            print(InvalidCsvProductError(str(e)))

    def get_products(self) -> pd.DataFrame:
        """Получение всех продуктов"""
        return self.products

    def get_product_by_id(self, id_product: int):
        """Получение продукта по ID"""
        if id_product not in self.products.index:
            return None
        row: pd.Series = self.products.loc[id_product]
        return row

    def get_products_by_id(self, products_id: list[int]) -> list[pd.Series | None]:
        """Получение списка продуктов по списку ID"""
        products: list[pd.Series | None] = []
        for id_product in products_id:
            products.append(self.get_product_by_id(id_product))
        return products

    def get_id_product_by_name(self, name_product: str) -> int | None:
        """Получение ID продукта по имени"""
        row: pd.DataFrame = self.products[self.products["name"] == name_product]
        if row.empty:
            return None
        return row.index[0]

    def get_info_product_by_id(self, product_id: int) -> pd.Series:
        """Получение информации о продукте по ID"""
        row: pd.Series = self.products.loc[product_id]
        return row

    def delete_product(self, id_product: int) -> None:
        """Удаление продукта и его изображения"""
        product = self.get_product_by_id(id_product)
        image_path: str = get_abs_path(product['image'])

        self.products.drop(id_product, inplace=True)

        if os.path.exists(image_path):
            os.remove(image_path)

        self.save()

    def add_product(self, name_product: str, price_product: int, path_product: str) -> None:
        """Добавление нового продукта и копирование изображения"""
        try:
            base_name: str = os.path.basename(path_product)
            relative_path: str = os.path.join("pictures", base_name)
            destination_path: str = get_abs_path("pictures", base_name)
            shutil.copyfile(path_product, destination_path)

            new_max_id: int = self.__get_max_id() + 1
            self.products.loc[new_max_id] = {
                'id': new_max_id,
                'name': name_product,
                'price': price_product,
                'image': relative_path
            }
            self.save()

        except Exception as e:
            print(InvalidAddProductError(str(e)))

    def __get_max_id(self) -> int:
        """Получение максимального ID продукта"""
        max_id: int = self.products.index.max()
        return max_id

    def save(self) -> None:
        """Сохраняет все изменения в CSV"""
        self.products.to_csv(
            self.file_path,
            index=True,
            index_label="id",
            encoding='UTF-8'
        )


if __name__ == "__main__":
    database_product_manager: DataBaseProductManager = DataBaseProductManager()
    print(database_product_manager.get_product_by_id(20))
    print(database_product_manager.get_info_product_by_id(3))
    # print(database_product_manager.delete_product(1))
