from boto3 import client
from botocore.exceptions import ClientError
import json
import botocore 
import psycopg2
import base64
import boto3
from .app_health import check_db_connection

instance_schedule = {
    "Instances": []
}


def get_scheduling():
    try:
        cursor = check_db_connection()
        postgreSQL_select_Query = "select ins.instance_id, ins.shutdown_time  from kanduladb.kanduladb.instances_scheduler ins ORDER BY ins.shutdown_time desc limit 20"

        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()
        for row in records:
                instance_schedule('Instances').append(instance_id = row[0] )
                instance_schedule('Instances').append(shutdown_hour = row[0] )

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        # closing database connection
        if cursor():
            cursor.close()
            cursor.close()
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
