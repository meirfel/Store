from flask import Blueprint, request

from db_models.customer import Customer

customer = Blueprint('customer', __name__)


@customer.route('/customer/sign_in', methods=['POST'])
def sign_in():
    credentials_dict = request.json()
    try:
        Customer.sign_in(**credentials_dict)
    except Exception as err:
        return err.args[0]


@customer.route('/customer/sign_up', methods=['POST'])
def sign_up():
    customer_details = request.json()
    try:
        new_customer = Customer(**customer_details)
        new_customer.insert_new_customer()
    except Exception as err:
        return err.args[0]
