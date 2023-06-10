import base64
from common.consts import VALID_REQUEST_PREFIX, INVALID_REQUEST_PREFIX

def encode_string(string_to_encrypt) -> str:
    message_bytes = string_to_encrypt.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message


def decode_string(data: str) -> str:
    base64_bytes = data.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message


def validate_number_is_positive(number: int) -> True:
    if number > 0:
        return True
    raise ValueError("Number is not positive")


def validate_string_contains_only_numbers(string: str):
    if string.isdigit():
        return True
    raise ValueError("Value should contain only numbers")


def create_valid_response(message: str):
    """ Return the message with the valid response in the beginning """
    return f"{VALID_REQUEST_PREFIX} {message}"


def create_invalid_response(message: str):
    """ Return the message with the invalid response in the beginning """
    return f"{INVALID_REQUEST_PREFIX} {message}"
