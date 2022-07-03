from boto3 import client
from botocore.exceptions import ClientError
import json
import botocore 
import botocore.session 
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig
import psycopg2

AWS_REGION="us-east-1"
ec2_client = client('ec2', region_name=AWS_REGION)

def get_machine_time():
    return 1602824750094  # No need to implement at the moment


def check_aws_connection():
    response = ec2_client.describe_instances()
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def check_db_connection():

    client = botocore.session.get_session().create_client('secretsmanager')
    cache_config = SecretCacheConfig()
    cache = SecretCache( config = cache_config, client = client)

    secret = cache.get_secret_string('kanduladblihi')
    secret_json=json.loads(secret)

    db_user=secret_json['username']
    db_pass=secret_json['password']
    db_name= secret_json['dbname']

    connection = psycopg2.connect(
    host = 'your_RDB_AWS_instance_Endpoint',
    port = 5432,
    user = 'YOUR_USER_NAME',
    password = 'YOUR_PASSWORD',
    database='YOUR_DATABASE_NAME'
    )
    cursor=connection.cursor()
    print ("hfkjdshflkdsahfdksjhfaksjdhf" + cursor)
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
