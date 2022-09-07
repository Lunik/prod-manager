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
from ProdManager import create_app

app = create_app()

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
        logger.info(f"[{monitor.name}] Ignoring")
        continue

      logger.info(f"[{monitor.name}] Handling monitor refresh")

      monitor_id = int(monitor.external_reference)
      logger.info(f"[{monitor.name}] Found Datadog monitor ID : {monitor_id}")

      try:
        monitor_state = api_instance.get_monitor(monitor_id)
      except NotFoundException as error:
        logger.error(f"[{monitor.name}] Datadog monitor with ID {monitor_id} was not found")
        continue


      status = monitor.status
      monitor_status = monitor_state.overall_state.to_str().lower()
      try:
        status = MonitorStatus(monitor_state.overall_state.to_str().lower())
        logger.info(f"[{monitor.name}] Datadog monitor status is : {status.name}")
      except ValueError:
        logger.warning(f"[{monitor.name}] Datadog monitor status is not handled : {monitor_status}")

      monitor, changed = update_resource(Monitor, monitor.id, dict(
        name=monitor_state.name,
        external_reference=monitor_state.id,
        external_link=f"https://{options['monitor_hostname']}/monitors/{monitor_state.id}",
        status=status
      ))

      if changed:
        logger.info(f"[{monitor.name}] Updating monitor status succeed")


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
    monitor_hostname=os.environ.get("DD_MONITOR_HOSTNAME", datadog_configuration.server_variables['site'])
  )

  process(integration_name, datadog_configuration, options)
