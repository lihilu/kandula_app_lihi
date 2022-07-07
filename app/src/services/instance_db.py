from boto3 import client
from botocore.exceptions import ClientError
import json
import psycopg2
from .app_health import db_host, aws_secret_manager
from .instance_data import InstanceData


AWS_REGION="us-east-1"
ec2_client = client('ec2', region_name=AWS_REGION)
response = ec2_client.describe_instances()
db_info=  aws_secret_manager('kanduladblihi')
conn = psycopg2.connect(database=db_info['dbname'],
                        host=db_host(),
                        user=db_info['username'],
                        password=db_info['password'],
                        port=5432)
def get_scheduling():
    instance_schedule = {
     "Instances": []
 }
    try:
        postgreSQL_select_Query = "select ins.instance_id, ins.shutdown_time  from kanduladb.kanduladb.instances_scheduler ins ORDER BY ins.shutdown_time desc limit 20"
        cur= conn.cursor()
        cur.execute(postgreSQL_select_Query)
        records = cur.fetchall()
          #  print (records)
        #    instance_schedule={'Instances':[]}
           # print ("emptyyyyy",instance_schedule)
        for row in records:
            if row[0] == 'None':
                continue
            single_instance={}
            single_instance['Id'] = row[0]
            single_instance['DailyShutdownHour'] = row[1]
              #  print ("single_instance", single_instance)
            instance_schedule['Instances'].append(single_instance)
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")
           # print (instance_schedule)
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    return instance_schedule


def create_scheduling(instance_id, shutdown_hour):
    instance_schedule = get_scheduling
    # instance_list_aws = response['Reservations'][0]['Instances']
    # print("AWS" , instance_list_aws)
    # instance_list_kandula= get_scheduling()
    # print ("kandula" ,instance_list_kandula)
    try:
        postgreSQL_select_Query = """
        insert into kanduladb.kanduladb.instances_scheduler (instance_id , shutdown_time)
        values (%s,%s)
        """
        record_to_insert = (instance_id,shutdown_hour)
        cur= conn.cursor()
        cur.execute(postgreSQL_select_Query, record_to_insert)
        conn.commit()
     
        count = cur.rowcount
        print(count, "Record inserted successfully into mobile table")       
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")
        index = [i['Id'] for i in instance_schedule["Instances"]].index(instance_id)
        instance_schedule["Instances"][index] = {"Id": instance_id, "DailyShutdownHour": int(shutdown_hour[0:2])}
        print("Instance {} will be shutdown was updated to the hour {}".format(instance_id, shutdown_hour))
    except Exception:  # insert
        instance_schedule["Instances"].append({"Id": instance_id, "DailyShutdownHour": int(shutdown_hour[0:2])})
        print("Instance {} will be shutdown every day when the hour is {}".format(instance_id, shutdown_hour))


def delete_scheduling(instance_id):
    instance_schedule = get_scheduling
    # TODO: Implement a delete query to remove the instance ID from scheduling
    try:
        index = [k['Id'] for k in instance_schedule["Instances"]].index(instance_id)
        instance_schedule["Instances"].pop(index)
        print("Instance {} was removed from scheduling".format(instance_id))
    except Exception:
        print("Instance {} was not there to begin with".format(instance_id))
