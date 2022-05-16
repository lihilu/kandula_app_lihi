from boto3 import client
ec2_client = client('ec2', region_name="us-east-1")

def get_machine_time():
    return 1602824750094  # No need to implement at the moment


def check_aws_connection():
    response = ec2_client.describe_instances()
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

def check_db_connection():
    # TODO: implement real select query to db. If successful, return true. otherwise return False
    return True


def is_app_healthy(healthchecks):
    return all([check["Value"] for check in healthchecks])


def get_app_health():
    health_checks = [
        {"Name": "machine-time", "Value": get_machine_time()},
        {"Name": "aws-connection", "Value": check_aws_connection()},
        {"Name": "db-connection", "Value": check_db_connection()},
    ]

    return health_checks, is_app_healthy(health_checks)