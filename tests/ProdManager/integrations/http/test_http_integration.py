
import random
import string
import json
import pytest
import responses

from requests.exceptions import ReadTimeout, ConnectionError, SSLError

from ProdManager.integrations.http.update_monitors import process as update_monitor_process
from ProdManager.helpers.resource import create_resource, get_resource
from ProdManager.models import Monitor, MonitorStatus
from ProdManager import create_app


app = create_app(scheduled_jobs=False)

MONITORS = dict()

def setup_function():
  with app.app_context():
    MONITORS["ignore"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="http",
      )
    ).id
    MONITORS["http"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="http",
        external_link="http://http.website"
      )
    ).id
    MONITORS["https"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="http",
        external_link="https://https.website"
      )
    ).id
    MONITORS["redirect"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="http",
        external_link="https://redirect.website"
      )
    ).id
    MONITORS["invalid_cert"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="http",
        external_link="https://invalid_cert.website"
      )
    ).id
    MONITORS["timeout"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="http",
        external_link="https://timeout.website"
      )
    ).id
    MONITORS["connection_refused"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="http",
        external_link="https://connection_refused.website"
      )
    ).id

@responses.activate
def test_process():

  responses.get("http://http.website", status=200)
  responses.get("https://https.website", status=200)
  responses.get("https://redirect.website", status=301)
  responses.get("https://invalid_cert.website", body=SSLError("UNITTEST SSL error"))
  responses.get("https://timeout.website", body=ReadTimeout("UNITTEST timeout"))
  responses.get("https://connection_refused.website", body=ConnectionError("UNITTEST connection refused"))


  update_monitor_process("http",
    configuration=dict(
      proxies=dict(),
      query_options=dict()
    )
  )

  with app.app_context():
    monitor = get_resource(Monitor, MONITORS["http"])
    assert monitor.status == MonitorStatus.OK

    monitor = get_resource(Monitor, MONITORS["https"])
    assert monitor.status == MonitorStatus.OK

    monitor = get_resource(Monitor, MONITORS["redirect"])
    assert monitor.status == MonitorStatus.OK

    monitor = get_resource(Monitor, MONITORS["invalid_cert"])
    assert monitor.status == MonitorStatus.ALERT

    monitor = get_resource(Monitor, MONITORS["timeout"])
    assert monitor.status == MonitorStatus.ALERT

    monitor = get_resource(Monitor, MONITORS["connection_refused"])
    assert monitor.status == MonitorStatus.ALERT