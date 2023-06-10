from dataclasses import dataclass
from typing import List, Optional, Any

from db_models.db_connection import DBConnection


@dataclass
class ProductColumns:
    PRODUCT_TABLE_NAME = "product"
    QUANTITIES_TABLE_NAME = "quantities"
    PRODUCT_ID = "product_id"
    NAME = "product_name"
    DESCRIPTION = "product_description"
    BRAND = "product_brand"
    CATEGORY = "product_category"
    PRICE = "product_price"
    AMOUNT = "product_amount"
    PRODUCT_ID_INDEX = 0
    NAME_INDEX = 1
    DESCRIPTION_INDEX = 2
    BRAND_INDEX = 3
    CATEGORY_INDEX = 4
    AMOUNT_INDEX = 6
    PRICE_INDEX = 7


class Product:
    """ Represents Product object form the DB """
    def __init__(self, product_id: str, name: str, description: str, brand: str, category: str, price: str, amount):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.brand = brand
        self.category = category
        self._price = price
        self._amount = amount

    @property
    def amount(self):
        query = {"query": f"SELECT q.{ProductColumns.AMOUNT} "
                          f"FROM {ProductColumns.QUANTITIES_TABLE_NAME} q, {ProductColumns.PRODUCT_TABLE_NAME} p "
                          f"WHERE q.{ProductColumns.PRODUCT_ID} = p.{ProductColumns.PRODUCT_ID} "
                          f"AND q.{ProductColumns.PRODUCT_ID} = %s",
                 "vars": (self.product_id,)}
        amount = DBConnection().execute_query(query_and_vars=query)
        return amount[0][0]

    def reduce_amount_of_product(self, amount_bought: int) -> bool:
        """ Reduces the amount of a specific product in the store"""
        new_amount = self.amount - amount_bought
        if new_amount < 0:
            raise ValueError("The amount you're trying to buy is bigger then the amount there is")
        return self.change_product_amount(new_amount=new_amount)

    def change_product_amount(self, new_amount):
        """ Changes the product quantity to the new one"""
        query_and_vars = {"query": f"UPDATE {ProductColumns.QUANTITIES_TABLE_NAME} "
                                   f"SET {ProductColumns.AMOUNT} = %s "
                                   f"WHERE {ProductColumns.PRODUCT_ID} = %s "
                                   f"RETURNING {ProductColumns.AMOUNT}",
                          "vars": (new_amount, self.product_id)}

        amount_in_db = DBConnection().execute_query(query_and_vars=query_and_vars, commit=True)[0][0]
        return amount_in_db == new_amount


    @staticmethod
    def get_all_products():
        lists_of_all_products = []
        query_and_vars = {"query": f"SELECT * FROM {ProductColumns.PRODUCT_TABLE_NAME} p, "
                                   f"{ProductColumns.QUANTITIES_TABLE_NAME} q "
                                   f"WHERE p.{ProductColumns.PRODUCT_ID} = q.{ProductColumns.PRODUCT_ID}"}
        products = DBConnection().execute_query(query_and_vars=query_and_vars)
        for product in products:
            lists_of_all_products.append(Product(product_id=product[ProductColumns.PRODUCT_ID_INDEX],
                                                 name=product[ProductColumns.NAME_INDEX],
                                                 description=product[ProductColumns.DESCRIPTION_INDEX],
                                                 brand=product[ProductColumns.BRAND_INDEX],
                                                 category=product[ProductColumns.CATEGORY_INDEX],
                                                 price=product[ProductColumns.PRICE_INDEX],
                                                 amount=float(product[ProductColumns.AMOUNT_INDEX])))
        return lists_of_all_products

    @staticmethod
    def get_available_products() -> List[Any]:
        """ Returns a list of products where the amount is bigger then 0 """
        all_products = Product.get_all_products()
        available_products = []
        for product in all_products:
            if product.amount > 0:
                available_products.append(product)
        return available_products

    @staticmethod
    def get_unavailable_products():
        """ Returns a list of products where the amount is lower then 1 """
        all_products = Product.get_all_products()
        unavailable_products = []
        for product in all_products:
            if product.amount < 1:
                unavailable_products.append(product)
        return unavailable_products

    @staticmethod
    def create_new_product(name, description, brand, category, amount, price):
        # TODO validate price and amount are positive
        query_and_vars = {"query": f"SELECT * FROM {ProductColumns.PRODUCT_TABLE_NAME} "
                                   f"WHERE {ProductColumns.NAME} = %s",
                          "vars": (name, )}
        if DBConnection().execute_query(query_and_vars=query_and_vars):
            raise Exception("Product with this name already exists")

        product_table_columns = ", ".join([ProductColumns.NAME, ProductColumns.DESCRIPTION, ProductColumns.BRAND,
                                           ProductColumns.CATEGORY])
        product_query_and_vars = {"query": f"INSERT INTO {ProductColumns.PRODUCT_TABLE_NAME} ({product_table_columns}) "
                                           f"VALUES (%s, %s, %s, %s) RETURNING {ProductColumns.PRODUCT_ID}",
                                  "vars": (name, description, brand, category)}
        product_id = DBConnection().execute_query(query_and_vars=product_query_and_vars, commit=True)[0][0]

        quantity_table_columns = ", ".join([ProductColumns.PRODUCT_ID, ProductColumns.AMOUNT, ProductColumns.PRICE])
        quantity_query_and_vars = {"query": f"INSERT INTO {ProductColumns.QUANTITIES_TABLE_NAME} "
                                            f"({quantity_table_columns}) "
                                            f"VALUES (%s, %s, %s) RETURNING {ProductColumns.PRODUCT_ID}",
                                   "vars": (product_id, amount, price)}
        DBConnection().execute_query(query_and_vars=quantity_query_and_vars, commit=True)


if __name__ == '__main__':
    a = Product.get_all_products()
    b =5