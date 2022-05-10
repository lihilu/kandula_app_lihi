"""Views module."""

from flask import render_template, flash, url_for, request
from dependency_injector.wiring import inject, Provide
from werkzeug.utils import redirect

from app.src.services import app_health, instance_shutdown_scheduling
from app.src.services.instance_actions import InstanceActions
from app.src.services.instance_data import InstanceData
from app.containers import Container

from botocore.exceptions import ClientError

from flask.views import MethodView

import logging

logger = logging.getLogger()


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


def home():
    logger.info("Home view")
    return render_template('home.html', title='Welcome to Kandula')


def about():
    return render_template('about.html', title='About')


def health():
    health_metrics, is_app_healthy = app_health.get_app_health()

    return render_template('health.html', title='Application Health',
                           healthchecks=health_metrics), 200 if is_app_healthy else 500


def metrics():
    return render_template('metrics.html', title='metrics', )


@inject
def instances(instance_data: InstanceData = Provide[Container.instance_data]):
    instances_response = instance_data.get_instances()
    return render_template('instances.html', title='Instances',
                           instances=instances_response['Instances'])


def scheduler():
    if request.method == 'POST':
        instance_shutdown_scheduling.handle_instance(request.form)

    scheduled_instances = instance_shutdown_scheduling.get_scheduled_instances()
    return render_template('scheduler.html', title='Scheduling',
                           scheduled_instances=scheduled_instances["Instances"])
