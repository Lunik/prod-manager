
import random
import string
import json
import pytest
from unittest import mock
from unittest.mock import MagicMock
from urllib3.response import HTTPResponse

from datadog_api_client import Configuration

from ProdManager.integrations.datadog.update_monitors import process as update_monitor_process
from ProdManager.helpers.resource import create_resource, get_resource
from ProdManager.models import Monitor, MonitorStatus
from ProdManager import create_app

app = create_app()

MONITORS = dict()

def setup_function():
  with app.app_context():
    MONITORS["ignore"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="datadog",
      )
    ).id
    MONITORS["10000001"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="datadog",
        external_reference="10000001"
      )
    ).id
    MONITORS["10000002"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="datadog",
        external_reference="10000002"
      )
    ).id
    MONITORS["10000003"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="datadog",
        external_reference="10000003"
      )
    ).id
    MONITORS["10000004"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="datadog",
        external_reference="10000004"
      )
    ).id
    MONITORS["10000005"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="datadog",
        external_reference="10000005"
      )
    ).id

def datadog_mock(method, url, *args, **kwargs):

  match url:
    case 'https://api.datadoghq.eu/api/v1/monitor/10000001':
      return HTTPResponse(body=json.dumps({"id": 10000001, "name": "01_TEST", "overall_state": "OK", "query": "no_query", "type": "synthetics alert"}).encode('utf-8'), status=200)
    case 'https://api.datadoghq.eu/api/v1/monitor/10000002':
      return HTTPResponse(body=json.dumps({"id": 10000002, "name": "02_TEST", "overall_state": "Warning", "query": "no_query", "type": "synthetics alert"}).encode('utf-8'), status=200)
    case 'https://api.datadoghq.eu/api/v1/monitor/10000003':
      return HTTPResponse(body=json.dumps({"id": 10000003, "name": "03_TEST", "overall_state": "Alert", "query": "no_query", "type": "synthetics alert"}).encode('utf-8'), status=200)
    case 'https://api.datadoghq.eu/api/v1/monitor/10000004':
      return HTTPResponse(body=json.dumps({"id": 10000004, "name": "04_TEST", "overall_state": "No Data", "query": "no_query", "type": "synthetics alert"}).encode('utf-8'), status=200)
    case 'https://api.datadoghq.eu/api/v1/monitor/10000005':
      return HTTPResponse(body=json.dumps({"errors": ["Monitor not found"]}).encode('utf-8'), status=404)

@mock.patch('urllib3.PoolManager.request')
def test_process(mock_instance):
  datadog_url = "https://datadoghq.eu"

  mock_instance.side_effect = datadog_mock
  #HTTPResponse(body=json.dumps({"id": 10000001, "name": "01_TEST", "overall_state": "OK", "query": "no_query", "type": "synthetics alert"}).encode('utf-8'), status=200)

  update_monitor_process("datadog", Configuration(
    api_key=dict(
      apiKeyAuth="XXXXX-API_KEY-XXXXX",
      appKeyAuth="XXXXX-APPLICATION_KEY-XXXXX",
    ),
    server_variables=dict(
      site="datadoghq.eu"
    ),
  ))

  with app.app_context():
    monitor = get_resource(Monitor, MONITORS["10000001"])
    assert monitor.name == "01_TEST"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link == f"{datadog_url}/monitors/10000001"

    monitor = get_resource(Monitor, MONITORS["10000002"])
    assert monitor.name == "02_TEST"
    assert monitor.status == MonitorStatus.WARNING
    assert monitor.external_link == f"{datadog_url}/monitors/10000002"

    monitor = get_resource(Monitor, MONITORS["10000003"])
    assert monitor.name == "03_TEST"
    assert monitor.status == MonitorStatus.ALERT
    assert monitor.external_link == f"{datadog_url}/monitors/10000003"

    monitor = get_resource(Monitor, MONITORS["10000004"])
    assert monitor.name == "04_TEST"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link == f"{datadog_url}/monitors/10000004"

    monitor = get_resource(Monitor, MONITORS["10000005"])
    assert monitor.name != "05_TEST"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link is None
