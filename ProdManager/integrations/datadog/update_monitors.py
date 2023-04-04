import os
import sys
import logging

from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.exceptions import NotFoundException

from ProdManager.models import (
  Monitor, MonitorStatus, Service, Scope,
  Incident, IncidentEvent, Maintenance, MaintenanceEvent,
)

from ProdManager.helpers.resource import list_resources, update_resource
from ProdManager.app import create_app

app = create_app(scheduled_jobs=False)

logger = logging.getLogger('Datadog')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel("INFO")

def process(integration_name, datadog_configuration, options):
  with ApiClient(datadog_configuration) as api_client:
    api_instance = MonitorsApi(api_client)

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

      monitor_id = int(monitor.external_reference)
      logger.info("[%s] Found Datadog monitor ID : %s", monitor.name, monitor_id)

      try:
        monitor_state = api_instance.get_monitor(monitor_id)
      except NotFoundException as error:
        logger.error("[%s] Datadog monitor with ID %s was not found", monitor.name, monitor_id)
        continue


      status = monitor.status
      monitor_status = monitor_state.overall_state.to_str().lower()
      try:
        status = MonitorStatus(monitor_state.overall_state.to_str().lower())
        logger.info("[%s] Datadog monitor status is : %s", monitor.name, status.name)
      except ValueError:
        logger.warning(
          "[%s] Datadog monitor status is not handled : %s", monitor.name, monitor_status
        )

      monitor, changed = update_resource(Monitor, monitor.id, dict(
        name=monitor_state.name,
        external_reference=monitor_state.id,
        external_link=f"https://{options['monitor_hostname']}/monitors/{monitor_state.id}",
        status=status
      ))

      if changed:
        logger.info("[%s] Updating monitor status succeed", monitor.name)


if __name__ == "__main__":
  datadog_configuration = Configuration(
    api_key=dict(
      apiKeyAuth=os.environ["DD_API_KEY"],
      appKeyAuth=os.environ["DD_APPLICATION_KEY"],
    ),
    server_variables=dict(
      site=os.environ.get("DD_SITE", "datadoghq.com")
    ),
  )

  integration_name="datadog"
  datadog_integration_suffix = os.environ.get("PM_INTEGRATION_SUFFIX")
  if datadog_integration_suffix:
    integration_name = f"{integration_name}_{datadog_integration_suffix}"

  options = dict(
    monitor_hostname=os.environ.get(
      "DD_MONITOR_HOSTNAME",
      datadog_configuration.server_variables['site'],
    )
  )

  process(integration_name, datadog_configuration, options)
