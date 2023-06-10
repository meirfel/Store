from flask import Flask, request, abort
import logging
import datetime
import json
from db_models.customer import CustomerColumns
from db_models.customer import Customer
from utils import encode_string
from common.logger import setup_app_logger
from common.customer import customer as customer_blueprint

# app = Flask(__name__)

# @app.route("/")
# def home():
#     meir_birth_date = datetime.datetime(year=1995, month=9, day=1).isoformat()
#     erik_birth_date = datetime.datetime(year=1997, month=4, day=6).isoformat()
#     yana_birth_date = datetime.datetime(year=1995, month=9, day=3).isoformat()
#     meir_json_as_string = {"name": "Meir", "birthDate": meir_birth_date}
#     erik_json_as_string = {"name": "Erik", "birthDate": erik_birth_date}
#     yana_json_as_string = {"name": "Yana", "birthDate": yana_birth_date}
#     return json.dumps([meir_json_as_string, erik_json_as_string, yana_json_as_string])


# @app.route("/getUser", methods=["POST"])
# def get_current_user():
#     print(request.data)
#     print(type(request.data))
#     my_json = request.data.decode('utf8').replace("'", '"')
#     data = json.loads(my_json)
#     print(f"Data is {data}")
#     answer = ""
#     try:
#         Customer.sign_in(id_number=data[CustomerColumns.CUSTOMER_ID], password=data[CustomerColumns.PASSWORD])
#         answer = "ok"
#     except Exception as err:
#         answer = f"ERROR: {err.args[0]}"
#    return answer

        # print(my_json[CustomerColumns.CUSTOMER_ID])
    # print(my_json[CustomerColumns.PASSWORD])

def create_app():
    """ Created the flask app """
    app = Flask(__name__)
    app.register_blueprint(customer_blueprint)
    setup_app_logger(app)
    app.run()


if __name__ == "__main__":
    create_app()

import psycopg2

# from db_models.customer import Customer
# import log
#
# log.setup_console()
# from log import logger
#
#
# def main():
#     customer = Customer(id_number="3", first_name="Yana", last_name="Feldman", email="yana627@gmail.com",
#                         address="Beer Sheva, Livna 14/43", password="Yana1995", phone_number="0508482636")
#     customer.insert_new_customer()
#     #customer.sign_in(id_number='1', password="123456")
#
#
# if __name__ == '__main__':
#     main()