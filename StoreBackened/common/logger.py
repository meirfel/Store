import logging
from logging import StreamHandler, FileHandler
from logging.handlers import RotatingFileHandler
import sys

GB_UNIT = 1024*1024*1024


def setup_app_logger(app=None, filename='reporter_service.log'):
    """Helper function that adds a file logger to the flask application.

    :param app: Flask application.
    :param filename: log file name.
    """
    format_string = '[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)d] %(message)s'
    init_logger(logging.INFO, filename, format_string)
    if app:
        app.logger.propagate = 1


def init_logger(log_level=logging.INFO, log_file_path=None, format_string=None, rotate_files=False, logger_class=None):
    if logger_class is not None:
        logging.setLoggerClass(logger_class)

    logger = logging.getLogger()
    if logger.handlers:
        logger.handlers = []
    if not format_string:
        format_string = '[%(name)s][%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'

    formatter = logging.Formatter(format_string)

    console_handler = StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    error_handler = StreamHandler(sys.stderr)
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    if log_file_path:

        if rotate_files:
            file_handler = RotatingFileHandler(
                filename=log_file_path,
                backupCount=30,
                maxBytes=GB_UNIT
            )
        else:
            file_handler = FileHandler(
                filename=log_file_path
            )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(log_level)