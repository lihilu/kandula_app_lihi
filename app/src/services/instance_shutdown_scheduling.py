from app.src.services.instance_db import create_scheduling, delete_scheduling, get_scheduling


def handle_instance(schedule_params):
    if schedule_params["instanceScheduleAction"] == "create":
        create_scheduling(schedule_params["instanceId"], schedule_params["shutdownHour"])
    elif schedule_params["instanceScheduleAction"] == "delete":
        delete_scheduling(schedule_params["instanceIdToRemove"])
    else:
        raise RuntimeError("Could not handle scheduling for given data: {}".format(schedule_params))


def get_scheduled_instances():
    return get_scheduling()
