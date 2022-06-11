import os
import re

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

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

datadog_configuration = Configuration(
  api_key=dict(
    apiKeyAuth=os.environ["DD_API_KEY"],
    appKeyAuth=os.environ["DD_APPLICATION_KEY"],
  ),
  server_variables=dict(
    site=os.environ.get("DD_SITE", "datadoghq.com")
  ),
)

database_engine = create_engine(os.environ.get(
  "PM_DATABASE_URI",
  "sqlite:///instance/ProManager.sqlite"
))

datadog_url_regex = re.compile(r".*/(\d+)$")

if __name__ == "__main__":
  with ApiClient(datadog_configuration) as api_client:
    api_instance = MonitorsApi(api_client)

  with Session(database_engine) as session:
    for monitor in session.scalars(select(Monitor).where(Monitor.external_link != "")):
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


      monitor_status = monitor_state.overall_state.to_str().lower()

      changed = False

      try:
        status = MonitorStatus(monitor_status)
        print(f"[INFO][{monitor.name}] Datadog monitor status is : {status.name}")
        if monitor.status != status:
          changed = True
          monitor.status = status
      except ValueError:
        print(f"[WARNING][{monitor.name}] Datadog monitor status is not handled : {monitor_status}")

      if monitor.name != monitor_state.name:
        changed = True
        monitor.name = monitor_state.name

      if changed:
        try:
          session.commit()
        except Exception as error:
          print(f"[ERROR][{monitor.name}] Unable to update monitor status : {error}")

        print(f"[INFO][{monitor.name}] Updating monitor status succeed")
