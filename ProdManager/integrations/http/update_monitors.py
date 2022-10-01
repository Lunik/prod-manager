import os
import sys
import re
import logging

from requests import Session
from requests.exceptions import ReadTimeout

from ProdManager.models import (
  Monitor, MonitorStatus, Service, Scope,
  Incident, IncidentEvent, Maintenance, MaintenanceEvent,
)

from ProdManager.helpers.config import boolean_param
from ProdManager.helpers.resource import list_resources, update_resource
from ProdManager.app import create_app

app = create_app()

logger = logging.getLogger('HTTP')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel("INFO")


def process(integration_name, configuration):
  session = Session()
  if len(configuration["proxies"]) > 0:
    session.proxies = configuration["proxies"]

  with app.app_context():
    for monitor in list_resources(
        Monitor,
        filters=(Monitor.integration == integration_name),
        paginate=False,
        limit=0
      ):

      if not monitor.external_link:
        logger.info("[%s] Ignoring", monitor.name)
        continue

      logger.info("[%s] Handling monitor refresh", monitor.name)

      http_url = monitor.external_link
      logger.info("[%s] Found monitor with HTTP link : %s", monitor.name, http_url)

      http_state = None
      try:
        http_state = session.get(http_url, **configuration['query_options'])
      except Exception as error:
        logger.error(error)

      translated_status = "alert"
      if http_state and (http_state.status_code >= 200 and http_state.status_code < 400):
        translated_status = "ok"

      status = MonitorStatus(translated_status)
      logger.info("[%s] HTTP monitor status is : %s", monitor.name, status.name)

      monitor, changed = update_resource(Monitor, monitor.id, dict(
        name=re.sub(r'^(\[https?\]\s?)?', '[HTTP] ', monitor.name, flags=re.IGNORECASE),
        external_link=http_url,
        status=status
      ))

      if changed:
        logger.info("[%s] Updating monitor status succeed", monitor.name)


if __name__ == "__main__":
  http_configuration = dict(
    proxies=dict(https=os.environ.get("HTTPS_PROXY"), http=os.environ.get("HTTP_PROXY")),
    query_options=dict(
      timeout=int(os.environ.get("HTTP_TIMEOUT", "5")),
      verify=boolean_param(os.environ.get("HTTP_VERIFY_CERT", 'True')),
      allow_redirects=boolean_param(os.environ.get("HTTP_ALLOW_REDIRECT", 'True')),
    )
  )

  integration_name="http"
  http_integration_suffix = os.environ.get("PM_INTEGRATION_SUFFIX")
  if http_integration_suffix:
    integration_name = f"{integration_name}_{http_integration_suffix}"

  process(integration_name, http_configuration)
