class Recommender:
    """Класс для рекомендации продуктов пользователю"""

    def __init__(self, database_product_manager: object, user_id: int = 0) -> None:
        self.database_product_manager = database_product_manager
        self.user_id: int = user_id

    def get_recommendation_products_id(self) -> list[int]:
        """Получение списка ID рекомендуемых продуктов"""
        products = self.database_product_manager.get_products()
        products_id: list[int] = products.index.tolist()
        return products_id


if __name__ == "__main__":
    from database import DataBaseProductManager

    database_product_manager: DataBaseProductManager = DataBaseProductManager()
    user_id: int = 0
    recommender: Recommender = Recommender(database_product_manager, user_id)
    recommender.get_recommendation_products_id()
