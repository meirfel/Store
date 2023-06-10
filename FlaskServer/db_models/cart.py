from dataclasses import dataclass
from db_models.db_connection import DBConnection


@dataclass
class CartColumns:
    TABLE_NAME = "cart"
    CUSTOMER_ID = "customer_id"
    PRODUCT_ID = "product_id"
    QUANTITY = "product_quantity"


class Cart:
    """ This class will handle customer services"""

    @staticmethod
    def get_user_cart(customer_id: str):
        """ Returns user's full cart list """
        query_and_vars = {"query": f"SELECT * FROM {CartColumns.TABLE_NAME} "
                                   f"WHERE {CartColumns.CUSTOMER_ID} = %s ",
                          "vars": (customer_id,)}
        return DBConnection().execute_query(query_and_vars=query_and_vars)


    @staticmethod
    def insert_new_item_to_cart(customer_id: str, product_id: str, product_quantity: int) -> None:
        """ Inserts product to the cart """
        table_columns = ", ".join([CartColumns.CUSTOMER_ID, CartColumns.PRODUCT_ID, CartColumns.QUANTITY])
        query_and_vars = {"query": f"INSERT INTO {CartColumns.TABLE_NAME} ({table_columns}) "
                                   f"VALUES (%s, %s, %s, ) RETURNING {CartColumns.CUSTOMER_ID}",
                          "vars": (customer_id, product_id, product_quantity)}
        DBConnection().execute_query(query_and_vars=query_and_vars, commit=True)

    @staticmethod
    def delete_item_from_cart(customer_id: str, product_id: str) -> None:
        """ Removed the item from the cart """
        query_and_vars = {"query": f"DELETE FROM {CartColumns.TABLE_NAME} "
                                   f"WHERE {CartColumns.PRODUCT_ID} = %s AND {CartColumns.CUSTOMER_ID} = %s",
                          "vars": (product_id, customer_id,)}
        DBConnection().execute_query(query_and_vars=query_and_vars, commit=True)
        query_and_vars = {"query": f"SELECT * FROM {CartColumns.TABLE_NAME} "
                                   f"WHERE {CartColumns.PRODUCT_ID} = %s AND {CartColumns.CUSTOMER_ID} = %s",
                          "vars": (product_id, customer_id)}
        if DBConnection().execute_query(query_and_vars=query_and_vars):
            raise Exception(f"Couldn't remove product id: {product_id} from cart")

    @staticmethod
    def update_quantity(customer_id: str, product_id: str, product_quantity: int):
        """ Updates the quantity of a specific product """
        query_and_vars = {"query": f"UPDATE {CartColumns.TABLE_NAME} "
                                   f"SET {CartColumns.QUANTITY} = %s "
                                   f"WHERE {CartColumns.PRODUCT_ID} = %s AND {CartColumns.CUSTOMER_ID} = %s"
                                   f"RETURNING {CartColumns.QUANTITY}",
                          "vars": (product_quantity, product_id, customer_id)}
        new_quantity = DBConnection().execute_query(query_and_vars=query_and_vars)
        if not new_quantity[0][0] == product_quantity:
            raise Exception("Couldn't update the quantity of the product")


