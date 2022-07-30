from os import environ
from app.application import create_app

app = create_app()

MANDATORY_ENV_VARIABLES = ["FLASK_ENV", "FLASK_APP", "SECRET_KEY", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]


def validate_mandatory_env_variables():
    for variable in MANDATORY_ENV_VARIABLES:
        if environ.get(variable) is None:
            raise SystemExit("ERROR: Kandula app must have a valid environment variable of {}. Exiting...".format(variable))


if __name__ == "__main__":
    validate_mandatory_env_variables()
    app.run(host='0.0.0.0', use_evalex=False)
