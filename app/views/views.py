"""Views module."""

from flask import render_template, flash, url_for, request
from dependency_injector.wiring import inject, Provide
from werkzeug.utils import redirect
from prometheus_client import Counter, Summary
import logging
from app.src.services import app_health, instance_shutdown_scheduling
from app.src.services.instance_actions import InstanceActions
from app.src.services.instance_data import InstanceData
from app.containers import Container

from botocore.exceptions import ClientError

from flask.views import MethodView


logger = logging.getLogger()


call_metric = Counter('opsschool_monitor_flask_number_of_requests', 'The total number of requests per-page', ['method', 'endpoint'])
time_metric = Summary('opsschool_monitor_flask_request_processing_seconds', 'Time spent processing request', [ 'endpoint' ])


class InstanceAPI(MethodView):
    @inject
    def __init__(self, instance_actions: InstanceActions = Provide[Container.instance_actions]) -> None:
        self.instance_actions = instance_actions
        super().__init__()


    def get(self, instance_id, instance_action):
        try:
            action_to_run = self.instance_actions.action_selector(instance_action)
            action_to_run(instance_id)
            flash("Your request to {} instance {} is in progress".format(instance_action, instance_id), "info")
        except (ClientError, RuntimeError) as e:
            flash("Cannot perform action '{}' on instance: {}".format(instance_action, instance_id), "danger")
            logger.exception(e)

        return redirect(url_for('instances'))

    def post(self, instance_id, instance_action):
        try:
            action_to_run = self.instance_actions.action_selector(instance_action)
            action_to_run(instance_id)
            flash("Your request to {} instance {} is in progress".format(instance_action, instance_id), "info")
        except (ClientError, RuntimeError) as e:
            flash("Cannot perform action '{}' on instance: {}".format(instance_action, instance_id), "danger")
            logger.exception(e)

        return redirect(url_for('instances'))


home_time = time_metric.labels(endpoint='home')
@home_time.time()
def home():
    logger.info("Home view")
    call_metric.labels(method='GET',endpoint='home').inc(1)
    return render_template('home.html', title='Welcome to Kandula')

about_time= time_metric.labels(endpoint='about')
@about_time.time()
def about():
    call_metric.labels(method='GET',endpoint='about').inc(1)
    return render_template('about.html', title='About')

health_time = time_metric.labels(endpoint='health')
@health_time.time()
def health():
    call_metric.labels(method='GET',endpoint='health').inc(1)
    health_metrics, is_app_healthy = app_health.get_app_health()

    return render_template('health.html', title='Application Health',
                           healthchecks=health_metrics), 200 if is_app_healthy else 500


metrics_time = time_metric.labels(endpoint='metrics')
@metrics_time.time()
def metrics():
    call_metric.labels(method='GET',endpoint='metrics').inc(1)
    return render_template('metrics.html', title='metrics', )


instances_time= time_metric.labels(endpoint='instances')

@inject
@instances_time.time()
def instances(instance_data: InstanceData = Provide[Container.instance_data]):
    instances_response = instance_data.get_instances()
    call_metric.labels(method='GET',endpoint='instances').inc(1)
    return render_template('instances.html', title='Instances',
                           instances=instances_response['Instances'])
@inject
def get_instance_list(instance_data: InstanceData = Provide[Container.instance_data]):
    instances_response = instance_data.get_instance_list()
    call_metric.labels(method='GET',endpoint='instances_list').inc(1)
    return instances_response


scheduler_time= time_metric.labels(endpoint='scheduler')
@scheduler_time.time()
def scheduler():
    if request.method == 'POST':
        instance_shutdown_scheduling.handle_instance(request.form)

    scheduled_instances = instance_shutdown_scheduling.get_scheduled_instances()
    call_metric.labels(method='GET',endpoint='scheduler').inc(1)
    return render_template('scheduler.html', title='Scheduling',
                           scheduled_instances=scheduled_instances["Instances"])

