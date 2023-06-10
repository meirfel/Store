from dataclasses import dataclass
import utils
from db_models.db_connection import DBConnection
from log import logger


@dataclass
class CustomerColumns:
    TABLE_NAME = "customer"
    CUSTOMER_ID = "customer_id"
    FIRST_NAME = "customer_first_name"
    LAST_NAME = "customer_last_name"
    EMAIL = "customer_email"
    PASSWORD = "customer_password"
    ADDRESS = "customer_address"
    PHONE = "customer_phone_number"
    CUSTOMER_ID_INDEX = 0
    FIRST_NAME_INDEX = 1
    LAST_NAME_INDEX = 2
    EMAIL_INDEX = 3
    PASSWORD_INDEX = 4
    ADDRESS_INDEX = 5
    PHONE_INDEX = 6


class Customer:
    """ This class will handle customer services"""

    def __init__(self, id_number: str, first_name: str, last_name: str, email: str, address: str, password: str,
                 phone_number: str):
        self.id_number = id_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.password = password
        self.phone_number = phone_number

    def validate_user_input(self):
        """ Validating user's input """
        # TODO validate user's input

    def insert_new_customer(self):
        """ Creating a new user in the DB """
        db_connection = DBConnection()
        table_columns = ", ".join([CustomerColumns.CUSTOMER_ID, CustomerColumns.FIRST_NAME, CustomerColumns.LAST_NAME,
                                   CustomerColumns.EMAIL, CustomerColumns.PASSWORD, CustomerColumns.ADDRESS,
                                   CustomerColumns.PHONE])
        query_and_vars = {"query": f"INSERT INTO {CustomerColumns.TABLE_NAME} ({table_columns}) "
                                   f"VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING {CustomerColumns.CUSTOMER_ID}",
                          "vars": (self.id_number, self.first_name, self.last_name, self.email,
                                   utils.encode_string(self.password), self.address, self.phone_number)}
        try:
            data = db_connection.execute_query(query_and_vars=query_and_vars, commit=True)
            print(f"Successfully inserted customer with id: {data[0][0]}, successfully")
            logger.debug(f"Inserted customer with id: {data[0]}, successfully")
        except Exception as err:
            logger.error(f"Couldn't add new customer due to: {err.args}")

    @staticmethod
    def sign_in(id_number: str, password: str) -> bool:

        query_and_vars = {"query": f"SELECT * FROM {CustomerColumns.TABLE_NAME} WHERE {CustomerColumns.CUSTOMER_ID}=%s",
                          "vars": (id_number,)}
        data = DBConnection().execute_query(query_and_vars=query_and_vars)
        if data:
            if data[0][CustomerColumns.PASSWORD_INDEX] == utils.encode_string(password):
                return True
            raise ValueError("Wrong Password")
        raise ValueError(f"The Id number: {id_number} doesn't exists")


