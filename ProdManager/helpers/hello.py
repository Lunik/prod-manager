import os
import logging
from datetime import datetime, timedelta

import requests

from ProdManager.plugins import scheduler
from ProdManager.models import (
  AppConfig, Service, Scope, Subscriber,
  Incident, Maintenance, Monitor, Announcement
)

class Hello:
  logger = logging.getLogger('gunicorn.error')
  endpoint = "https://hello.prod-manager.tiwabbit.fr"

  def __init__(self, app, refresh_interval_days=7, next_run_time_delta_seconds=30):
    if os.environ.get("FLASK_RUN_FROM_CLI"):
      return

    if os.environ.get("PM_HELLO_ENDPOINT"):
      self.endpoint = os.environ.get("PM_HELLO_ENDPOINT")

    if app.config["DISABLE_HELLO"]:
      self.logger.info("Hello has been disabled")
    else:
      scheduler.add_job(
        self.hello,
        'interval',
        days=refresh_interval_days,
        next_run_time=datetime.now() + timedelta(seconds=next_run_time_delta_seconds),
        name="Hello",
        coalesce=True,
        max_instances=1,
        args=(self, app,)
      )

  @staticmethod
  def generate_playload(app):
    with app.app_context():
      playload = dict(
        uuid=AppConfig.query.first().uuid,
        version=f"v{app.version.current.base_version}",
        lang=app.config["LANG"],
        counts=dict(
          services=Service.query.count(),
          scopes=Scope.query.count(),
          incidents=Incident.query.count(),
          maintenances=Maintenance.query.count(),
          announcements=Announcement.query.count(),
          monitors=Monitor.query.count(),
          subscribers=Subscriber.query.count(),
        ),
        features=dict(
          mail=app.config["MAIL_ENABLED"],
          api_rate_limit=app.config["API_RATELIMIT_ENABLED"],
          version_check=not app.config["DISABLE_VERSION_CHECK"]
        ),
        integrations=dict(
          datadog=Monitor.query.filter(Monitor.integration.startswith("datadog")).count(),
          dns=Monitor.query.filter(Monitor.integration.startswith("dns")).count(),
          http=Monitor.query.filter(Monitor.integration.startswith("http")).count(),
          jenkins=Monitor.query.filter(Monitor.integration.startswith("jenkins")).count(),
        )
      )

    return playload

  @staticmethod
  def hello(hello, app):
    try:
      playload = Hello.generate_playload(app)
    except Exception as error:
      hello.logger.debug("Failed to generate Hello playload")
      hello.logger.debug(error)
      return

    try:
      response = requests.post(hello.endpoint, json=playload, timeout=300)
    except Exception as error:
      hello.logger.debug("Failed to send Hello playload")
      hello.logger.debug(error)
      return

    return response
