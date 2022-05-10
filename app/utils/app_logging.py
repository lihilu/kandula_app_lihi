import logging
import sys

import json_logging


def init_logging():
    json_logging.init_flask(enable_json=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    file_handler = logging.handlers.RotatingFileHandler(filename='kandula.log', maxBytes=5000000, backupCount=10)
    logger.addHandler(file_handler)
