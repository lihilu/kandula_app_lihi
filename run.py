from os import environ
from app.application import create_app
import argparse
import logging
from prometheus_client import start_http_server
from sqlalchemy import true


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--semester', default='unspecified')
parser.add_argument('-b', '--bind', default='0.0.0.0')
parser.add_argument('-p', '--port', default='9200')
parser.add_argument('-l', '--log', default='info', choices=['debug', 'info', 'warning'])
args = parser.parse_args()


# log config
logging.basicConfig(format='%(asctime)s: %(message)s')
logger = logging.getLogger("ExtractDeviceMetrics")
if args.log == "info":
    logger.setLevel(logging.INFO)
elif args.log == "debug":
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARNING)



app = create_app()

MANDATORY_ENV_VARIABLES = ["FLASK_ENV", "FLASK_APP", "SECRET_KEY", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]


def validate_mandatory_env_variables():
    for variable in MANDATORY_ENV_VARIABLES:
        if environ.get(variable) is None:
            raise SystemExit("ERROR: Kandula app must have a valid environment variable of {}. Exiting...".format(variable))


if __name__ == "__main__":
    validate_mandatory_env_variables()
    start_http_server(9100)
    app.run(host='0.0.0.0', use_evalex=False, debug=true)
