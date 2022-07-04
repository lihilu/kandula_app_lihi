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


instance_schedule = {
    "Instances": [
        {"Id": "i-1234567890abcdef0", "DailyShutdownHour": 23},
        {"Id": "i-0ea8205a7a93969a5", "DailyShutdownHour": 20},
        {"Id": "i-05d648b954c1254d6", "DailyShutdownHour": 18}
    ]
}


def get_scheduling():
    try:
        db_info=aws_secret_manager('kanduladblihi')
        conn = psycopg2.connect(database=db_info['dbname'],
                            host=db_host(),
                            user=db_info['username'],
                            password=db_info['password'],
                            port=5432)
        cursor = conn.cursor()
        postgreSQL_select_Query = "select * from mobile where id = %s"

        cursor.execute(postgreSQL_select_Query, (mobileID,))
        mobile_records = cursor.fetchall()
        for row in mobile_records:
                print("Id = ", row[0], )
                print("Model = ", row[1])
                print("Price  = ", row[2])

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        # closing database connection
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed \n")
    # TODO: Implement a DB select query that gets all instance ids and their scheduled hours
    #       The returned data would be a in JSON format as show in the sample output below
    return instance_schedule


def create_scheduling(instance_id, shutdown_hour):
    # TODO: Implement a DB insert that creates the instance ID and the chosen hour in DB
    try:  # update
        index = [i['Id'] for i in instance_schedule["Instances"]].index(instance_id)
        instance_schedule["Instances"][index] = {"Id": instance_id, "DailyShutdownHour": int(shutdown_hour[0:2])}
        print("Instance {} will be shutdown was updated to the hour {}".format(instance_id, shutdown_hour))
    except Exception:  # insert
        instance_schedule["Instances"].append({"Id": instance_id, "DailyShutdownHour": int(shutdown_hour[0:2])})
        print("Instance {} will be shutdown every day when the hour is {}".format(instance_id, shutdown_hour))


def delete_scheduling(instance_id):
    # TODO: Implement a delete query to remove the instance ID from scheduling
    try:
        index = [k['Id'] for k in instance_schedule["Instances"]].index(instance_id)
        instance_schedule["Instances"].pop(index)
        print("Instance {} was removed from scheduling".format(instance_id))
    except Exception:
        print("Instance {} was not there to begin with".format(instance_id))
