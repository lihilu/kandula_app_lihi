from boto3 import client
from botocore.exceptions import ClientError
import json
import botocore 
import psycopg2
import base64
import boto3
from app_health import db_host , aws_secret_manager

instance_schedule = {
    "Instances": [
        {"Id": "i-1234567890abcdef0", "DailyShutdownHour": 23},
        {"Id": "i-0ea8205a7a93969a5", "DailyShutdownHour": 20},
        {"Id": "i-05d648b954c1254d6", "DailyShutdownHour": 18}
    ]
}

def db_connection():
    db_info=  aws_secret_manager('kanduladblihi')
    conn = psycopg2.connect(database=db_info['dbname'],
                        host=db_host(),
                        user=db_info['username'],
                        password=db_info['password'],
                        port=5432)
    return (conn)

def get_scheduling():
    try:
        cursor = db_connection.conn()
        postgreSQL_select_Query = "select ins.instance_id, ins.shutdown_time  from kanduladb.kanduladb.instances_scheduler ins ORDER BY ins.shutdown_time desc limit 20"

        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()
        for row in records:
                print("Id ", row[0], )
                print("DailyShutdownHour", row[1])

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        # closing database connection
        if db_connection.conn():
            cursor.close()
            db_connection.conn().close()
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
