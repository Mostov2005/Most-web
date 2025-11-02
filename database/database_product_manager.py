import pandas as pd
import os
import shutil
from utils import InvalidJsonError
from core import PasswordHasher
from database.get_abs_path import get_abs_path
from utils import InvalidAddProductError


class DataBaseProductManager:
    def __init__(self):
        self.products = pd.DataFrame()
        self.ph = PasswordHasher
        self.file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'system_file', 'products.csv')
        )
        self.__read_products()
        # print(self.products)
        # print(self.products.info())

    def __read_products(self):
        try:
            self.products = pd.read_csv(self.file_path, encoding='UTF-8', index_col="id")
        except Exception as e:
            print(InvalidJsonError(str(e)))

    def get_products(self):
        return self.products

    def get_product_by_id(self, id_product):
        if id_product not in self.products.index:
            return None
        row = self.products.loc[id_product]
        return row

    def get_products_by_id(self, products_id: list) -> list:
        products = []
        for id_product in products_id:
            products.append(self.get_product_by_id(id_product))
        return products

    def get_id_product_by_name(self, name_product: str) -> None:
        row = self.products[self.products["name"] == name_product]
        # print(row)

        if row.empty:
            return None
        return row.index[0]

    def delete_product(self, id_product: int) -> None:
        product = self.get_product_by_id(id_product)
        image_path = get_abs_path(product['image'])

        self.products.drop(id_product, inplace=True)
        self.products.reset_index(drop=True, inplace=True)

        if os.path.exists(image_path):
            os.remove(image_path)

        self.save()

    def add_product(self, name_product, price_product: int, path_product):
        try:
            # Копируем изображение в папку с изображениями
            base_name = os.path.basename(path_product)
            relative_path = os.path.join("pictures", base_name)
            destination_path = get_abs_path("pictures", base_name)
            shutil.copyfile(path_product, destination_path)

            new_max_id = self.__get_max_id() + 1
            self.products.loc[len(self.products)] = {
                'id': new_max_id,
                'name': name_product,
                'price': price_product,
                'image': relative_path
            }
            self.save()

        except Exception as e:
            print(InvalidAddProductError(str(e)))

    def __get_max_id(self):
        max_id = self.products.index.max()
        return max_id

    def save(self):
        """Сохраняет все изменения в CSV."""
        self.products.to_csv(self.file_path, index=True, index_label="id", encoding='UTF-8')


if __name__ == "__main__":
    database_product_manager = DataBaseProductManager()
    print(database_product_manager.get_product_by_id(20))
    print(database_product_manager.get_id_product_by_name('Носки'))
    # print(database_product_manager.delete_product(1))
