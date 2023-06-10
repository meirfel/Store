from flask import Blueprint, request

from db_models.customer import Customer
from utils import create_valid_response, create_invalid_response
customer = Blueprint('customer', __name__)


@customer.route('/customer/sign_in', methods=['POST'])
def sign_in():
    credentials_dict = request.json
    try:
        first_name = Customer.sign_in(**credentials_dict)
        return create_valid_response(message=first_name)
    except Exception as err:
        return err.args[0]


@customer.route('/customer/sign_up', methods=['POST'])
def sign_up():
    customer_details = request.json
    try:
        new_customer = Customer(**customer_details)
        new_customer.insert_new_customer()
        return create_valid_response(message=f"Created a new user {customer_details}")
    except Exception as err:
        return create_invalid_response(f"Couldn't create a new user due to, {err.args[0]}")
