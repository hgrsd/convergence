import datetime
import logging


def log_error(error):
    logging.error(f"{_current_date()}: {error}")


def log_info(info):
    logging.info(f"{_current_date()}: {info}")


def _current_date():
    return datetime.datetime.utcnow().isoformat()
