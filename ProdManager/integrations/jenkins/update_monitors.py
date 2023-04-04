import os
import sys
import logging

from api4jenkins import Jenkins
from api4jenkins.exceptions import AuthenticationError
from api4jenkins.job import Folder

from ProdManager.models import (
  Monitor, MonitorStatus, Service, Scope,
  Incident, IncidentEvent, Maintenance, MaintenanceEvent,
)

from ProdManager.helpers.resource import list_resources, update_resource
from ProdManager.app import create_app

app = create_app(scheduled_jobs=False)

logger = logging.getLogger('Jenkins')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel("INFO")


JENKINS_MONITOR_STATUSES = dict(
  SUCCESS="ok",
  UNSTABLE="warning",
  FAILURE="alert",
)


def process(integration_name, configuration):
  api_instance = Jenkins(**configuration)

  try:
    logger.info("Jenkins version : %s", api_instance.version)
  except AuthenticationError as error:
    logger.error(error)
    sys.exit(1)

  with app.app_context():
    for monitor in list_resources(
        Monitor,
        filters=(Monitor.integration == integration_name),
        paginate=False,
        limit=0
      ):

      if not monitor.external_reference:
        logger.info("[%s] Ignoring", monitor.name)
        continue

      logger.info("[%s] Handling monitor refresh", monitor.name)

      job_path = monitor.external_reference
      logger.info("[%s] Found monitor with Jenkins job path : %s", monitor.name, job_path)

      job_state = api_instance.get_job(job_path)
      if job_state is None:
        logger.error("[%s] Jenkins job with path %s was not found", monitor.name, job_path)
        continue

      if isinstance(job_state, Folder):
        logger.error("[%s] Jenkins job with path %s is a folder", monitor.name, job_path)
        continue

      status = monitor.status

      job_last_completed_build = job_state.get_last_completed_build()
      if job_last_completed_build is None:
        logger.warning("[%s] Jenkins job with path %s has no build", monitor.name, job_path)
      else:
        job_last_completed_build_result = job_last_completed_build.result
        try:
          translated_status = JENKINS_MONITOR_STATUSES[job_last_completed_build_result]
          status = MonitorStatus(translated_status)
          logger.info("[%s] Jenkins monitor status is : %s", monitor.name, status.name)
        except KeyError:
          logger.warning(
            "[%s] Jenkins monitor status is not handled : %s",
            monitor.name,
            job_last_completed_build_result,
          )
          continue

      monitor, changed = update_resource(Monitor, monitor.id, dict(
        name=job_state.display_name,
        external_reference=job_path,
        external_link=job_state.url,
        status=status
      ))

      if changed:
        logger.info("[%s] Updating monitor status succeed", monitor.name)


if __name__ == "__main__":
  jenkins_configuration = dict(
    url=os.environ["JENKINS_URL"],
    auth=(
      os.environ["JENKINS_USERNAME"],
      os.environ["JENKINS_TOKEN"]
    )
  )

  integration_name="jenkins"
  jenkins_integration_suffix = os.environ.get("PM_INTEGRATION_SUFFIX")
  if jenkins_integration_suffix:
    integration_name = f"{integration_name}_{jenkins_integration_suffix}"

  process(integration_name, jenkins_configuration)
