import os
import sys
import logging
import dns.resolver
import dns.rdtypes

from ProdManager.models import (
  Monitor, MonitorStatus, Service, Scope,
  Incident, IncidentEvent, Maintenance, MaintenanceEvent,
)

from ProdManager.helpers.resource import list_resources, update_resource
from ProdManager.app import create_app

app = create_app()

logger = logging.getLogger('DNS')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'))
logger.addHandler(handler)
logger.setLevel("INFO")

DNS_MONITOR_STATUSES = ["alert", "ok"]

def query(qname, resolver, rdtype="A"):
  logger.info("Searching for %s IN %s", qname, rdtype)
  result = []

  try:
    answer = resolver.resolve(qname, rdtype)
    match rdtype:
      case "A":
        result = [rr.address for rr in answer]
      case "CNAME":
        result = [rr.target for rr in answer]
  except dns.resolver.NoAnswer as error:
    logger.info(error)
    if rdtype == "CNAME":
      raise error

    answer = query(qname, resolver, rdtype="CNAME")
    result = query(answer[0], resolver, rdtype)
  except dns.resolver.NXDOMAIN as error:
    logger.error(error)

  return result


def process(integration_name, configuration):
  resolver = dns.resolver.Resolver(configure=True)
  if len(configuration["nameservers"]) > 0:
    resolver.nameservers = configuration["nameservers"]
  resolver.port = configuration["port"]

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

      dns_name = monitor.external_reference
      logger.info("[%s] Found monitor with DNS record : %s", monitor.name, dns_name)

      try:
        dns_state = query(dns_name, resolver)
      except Exception as error:
        logger.error(error)
        dns_state = []

      dns_found_result = len(dns_state) > 0

      status = monitor.status
      try:
        translated_status = DNS_MONITOR_STATUSES[int(dns_found_result)]
        status = MonitorStatus(translated_status)
        logger.info("[%s] DNS monitor status is : %s", monitor.name, status.name)
      except KeyError:
        logger.warning(
          "[%s] DNS monitor status is not handled : %s",
          monitor.name,
          translated_status
        )
        continue

      monitor, changed = update_resource(Monitor, monitor.id, dict(
        name=f"[DNS] {dns_name}",
        external_reference=dns_name,
        external_link=f"ip://{dns_state[0]}" if dns_found_result else "",
        status=status
      ))

      if changed:
        logger.info("[%s] Updating monitor status succeed", monitor.name)


if __name__ == "__main__":
  dns_configuration = dict(
    nameservers=list(filter(len, os.environ.get('DNS_NAMESERVERS', '').split(','))),
    port=int(os.environ.get('DNS_PORT', '53'))
  )

  integration_name="dns"
  dns_integration_suffix = os.environ.get("PM_INTEGRATION_SUFFIX")
  if dns_integration_suffix:
    integration_name = f"{integration_name}_{dns_integration_suffix}"

  process(integration_name, dns_configuration)
