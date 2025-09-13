class Recommender:
    def __init__(self, database_product_manager, user_id = 0):
        self.database_product_manager = database_product_manager
        self.user_id = user_id

    def get_recommendation_products_id(self):
        products = self.database_product_manager.get_products()
        products_id = products.index.tolist()
        return products_id


if __name__ == "__main__":
    from database import DataBaseProductManager
    database_product_manager = DataBaseProductManager()
    user_id = 0
    recommender = Recommender(database_product_manager, user_id)
    recommender.get_recommendation_products_id()
