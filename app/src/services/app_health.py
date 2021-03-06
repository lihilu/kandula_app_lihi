from boto3 import client
from botocore.exceptions import ClientError
import json
import botocore 
import psycopg2
import base64
import boto3

AWS_REGION="us-east-1"
ec2_client = client('ec2', region_name=AWS_REGION)
db_instance = 'kanduladb'

def get_machine_time():
    return 1602824750094  # No need to implement at the moment


def check_aws_connection():
    response = ec2_client.describe_instances()
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def aws_secret_manager(secretid):
    client = botocore.session.get_session().create_client('secretsmanager')
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secretid)
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    secret_load= json.loads(secret)  # returns the secret as dictionary
    return (secret_load)


def db_host():
    client = boto3.client('rds', region_name=AWS_REGION)
    db_instances = client.describe_db_instances()
    rds_host = db_instances.get('DBInstances')[0].get('Endpoint').get('Address')
    return (rds_host)

def check_db_connection():
    db_info=  aws_secret_manager('kanduladblihi')
    try:
        conn = psycopg2.connect(database=db_info['dbname'],
                        host=db_host(),
                        user=db_info['username'],
                        password=db_info['password'],
                        port=5432)
        conn.close()
        return True
    except:
        return False


def is_app_healthy(healthchecks):
    return all([check["Value"] for check in healthchecks])


def get_app_health():
    health_checks = [
        {"Name": "machine-time", "Value": get_machine_time()},
        {"Name": "aws-connection", "Value": check_aws_connection()},
        {"Name": "db-connection", "Value": check_db_connection()},
    ]

    return health_checks, is_app_healthy(health_checks)
