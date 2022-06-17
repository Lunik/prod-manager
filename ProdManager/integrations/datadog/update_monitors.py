import os
import re

from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.exceptions import NotFoundException

from ProdManager.models.Monitor import Monitor, MonitorStatus
from ProdManager.models.Service import Service
from ProdManager.models.Scope import Scope
from ProdManager.models.Incident import Incident
from ProdManager.models.IncidentEvent import IncidentEvent
from ProdManager.models.Maintenance import Maintenance
from ProdManager.models.MaintenanceEvent import MaintenanceEvent

from ProdManager.helpers.resource import list_resources, update_resource
from ProdManager import create_app

app = create_app()

datadog_configuration = Configuration(
  api_key=dict(
    apiKeyAuth=os.environ["DD_API_KEY"],
    appKeyAuth=os.environ["DD_APPLICATION_KEY"],
  ),
  server_variables=dict(
    site=os.environ.get("DD_SITE", "datadoghq.com")
  ),
)

datadog_url_regex = re.compile(r".*/(\d+)$")

if __name__ == "__main__":
  with ApiClient(datadog_configuration) as api_client:
    api_instance = MonitorsApi(api_client)

  with app.app_context():
    for monitor in list_resources(Monitor, paginate=False):

      if not monitor.external_link:
        print(f"[INFO][{monitor.name}] Ignoring")
        continue

      print(f"[INFO][{monitor.name}] Handling monitor refresh")

      matched_url = datadog_url_regex.match(monitor.external_link)
      if not matched_url:
        print(f"[WARNING][{monitor.name}] External link is not a valid Datadog monitor URL : {monitor.external_link}")
        continue

      monitor_id = int(datadog_url_regex.match(monitor.external_link).group(1))
      print(f"[INFO][{monitor.name}] Found Datadog monitor ID : {monitor_id}")

      try:
        monitor_state = api_instance.get_monitor(monitor_id)
      except NotFoundException as error:
        print(f"[ERROR][{monitor.name}] Datadog monitor with ID {monitor_id} was not found")
        continue


      status = monitor.status
      monitor_status = monitor_state.overall_state.to_str().lower()
      try:
        status = MonitorStatus(monitor_state.overall_state.to_str().lower())
        print(f"[INFO][{monitor.name}] Datadog monitor status is : {status.name}")
      except ValueError:
        print(f"[WARNING][{monitor.name}] Datadog monitor status is not handled : {monitor_status}")


      monitor, changed = update_resource(Monitor, monitor.id, dict(
        name=monitor_state.name,
        status=status
      ))

      if changed:
        print(f"[INFO][{monitor.name}] Updating monitor status succeed")
