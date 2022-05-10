instance_schedule = {
    "Instances": [
        {"Id": "i-1234567890abcdef0", "DailyShutdownHour": 23},
        {"Id": "i-0ea8205a7a93969a5", "DailyShutdownHour": 20},
        {"Id": "i-05d648b954c1254d6", "DailyShutdownHour": 18}
    ]
}


def get_scheduling():
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
