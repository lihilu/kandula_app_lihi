"""Application module."""
import os
from datetime import datetime

from flask import Flask
from flask_bootstrap import Bootstrap

from .containers import Container
from .utils.app_logging import init_logging
from .views import views
from .views.views import InstanceAPI


def create_app() -> Flask:
    container = Container()
    container.config.from_yaml('config.yml')
    container.config.aws_access_key_id.from_env('AWS_ACCESS_KEY_ID')
    container.config.aws_secret_access_key.from_env('AWS_SECRET_ACCESS_KEY')
    container.config.aws_session_token.from_env('AWS_SESSION_TOKEN')
    container.wire(packages=[views])

    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY')

    app.container = container

    app.add_url_rule('/', 'home', views.home, methods=['GET'])
    app.add_url_rule('/home', 'home', views.home, methods=['GET'])
    app.add_url_rule('/scheduler', 'scheduler', views.scheduler, methods=['GET', 'POST'])
    app.add_url_rule('/metrics', 'metrics', views.metrics, methods=['GET'])
    app.add_url_rule('/about', 'about', views.about, methods=['GET'])
    app.add_url_rule('/health', 'health', views.health, methods=['GET'])
    app.add_url_rule('/instances', 'instances', views.instances, methods=['GET'])
    app.add_url_rule('/instances/<string:instance_id>/<string:instance_action>',
                     view_func=InstanceAPI.as_view('instance_actions'), methods=['GET', 'POST'])

    with app.app_context():
        @app.template_filter()
        def format_datetime(timestamp):
            date_value = datetime.fromtimestamp(timestamp / 1000)
            return date_value.strftime("%d/%m/%y %H:%M:%S")

        @app.template_filter()
        def today_scheduling(hour):
            now = datetime.now()
            today_scheduling_time = now.replace(second=0, microsecond=0, minute=0, hour=hour)
            return today_scheduling_time.strftime("%d/%m/%y %H:%M:%S")

        init_logging()

    bootstrap = Bootstrap()
    bootstrap.init_app(app)

    return app
