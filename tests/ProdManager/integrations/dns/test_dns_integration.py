
import random
import string
import json
import pytest
from unittest import mock
from unittest.mock import MagicMock
from urllib3.response import HTTPResponse

import dns.resolver
import dns.rdatatype
import dns.rdataclass
import dns.message
import dns.name

from ProdManager.integrations.dns.update_monitors import process as update_monitor_process
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
        integration="dns",
      )
    ).id
    MONITORS["a.local"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="dns",
        external_reference="a.local"
      )
    ).id
    MONITORS["cname.local"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="dns",
        external_reference="cname.local"
      )
    ).id
    MONITORS["cname.cname.local"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="dns",
        external_reference="cname.cname.local"
      )
    ).id
    MONITORS["nxdomain.local"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="dns",
        external_reference="nxdomain.local"
      )
    ).id
    MONITORS["nxdomain.cname.local"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="dns",
        external_reference="nxdomain.cname.local"
      )
    ).id
    MONITORS["noanswer.local"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="dns",
        external_reference="noanswer.local"
      )
    ).id
    MONITORS["noanswer.cname.local"] = create_resource(
      Monitor,
      dict(
        name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        scope_id=1,
        service_id=1,
        integration="dns",
        external_reference="noanswer.cname.local"
      )
    ).id

def dns_mock(qname, rdtype, *args, **kwargs):
  if type(qname) is dns.name.Name:
    qname = qname.to_text(omit_final_dot=True)

  query = dns.message.make_query(qname, rdtype)
  response = dns.message.make_response(query)

  if rdtype == "A":
    if qname not in ["a.local"]:
      if qname in ["nxdomain.local"]:
        raise dns.resolver.NXDOMAIN(f"The DNS query name does not exist:  {qname}.")
      else:
        raise dns.resolver.NoAnswer(f"The DNS response does not contain an answer to the question: {qname}. IN A")

    rrs = dns.rrset.from_text(
      qname, 5, "IN", "A", "127.0.0.1"
    )
    answer = dns.resolver.Answer(qname, dns.rdatatype.A, dns.rdataclass.IN, response)

  elif rdtype == "CNAME":
    if qname not in ["cname.local", "cname.cname.local", "nxdomain.cname.local"]:
      raise dns.resolver.NoAnswer(f"The DNS response does not contain an answer to the question: {qname}. IN CNAME")

    targets = {
      "cname.local": "a.local",
      "cname.cname.local": "cname.local",
      "nxdomain.cname.local": "nxdomain.local",
      "noanswer.cname.local": "noanswer.local"
    }
    rrs = dns.rrset.from_text(
      qname, 5, "IN", "CNAME", targets[qname]
    )
        
    answer = dns.resolver.Answer(qname, dns.rdatatype.CNAME, dns.rdataclass.IN, response)

  response.answer.append(rrs)
  answer.rrset = rrs
  return answer

@mock.patch('dns.resolver.Resolver')
def test_process(mock_class):

  mock_instance = mock_class.return_value

  mock_instance.resolve.side_effect = dns_mock

  update_monitor_process("dns",
    configuration=dict(
      nameservers=[],
      port=53
    )
  )

  with app.app_context():
    monitor = get_resource(Monitor, MONITORS["a.local"])
    assert monitor.name == "[DNS] a.local"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link == "ip://127.0.0.1"

    monitor = get_resource(Monitor, MONITORS["cname.local"])
    assert monitor.name == "[DNS] cname.local"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link == "ip://127.0.0.1"

    monitor = get_resource(Monitor, MONITORS["cname.cname.local"])
    assert monitor.name == "[DNS] cname.cname.local"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link == "ip://127.0.0.1"

    monitor = get_resource(Monitor, MONITORS["nxdomain.local"])
    assert monitor.name == "[DNS] nxdomain.local"
    assert monitor.status == MonitorStatus.ALERT
    assert monitor.external_link == ""

    monitor = get_resource(Monitor, MONITORS["nxdomain.cname.local"])
    assert monitor.name == "[DNS] nxdomain.cname.local"
    assert monitor.status == MonitorStatus.ALERT
    assert monitor.external_link == ""

    monitor = get_resource(Monitor, MONITORS["noanswer.local"])
    assert monitor.name == "[DNS] noanswer.local"
    assert monitor.status == MonitorStatus.ALERT
    assert monitor.external_link == ""

    monitor = get_resource(Monitor, MONITORS["noanswer.cname.local"])
    assert monitor.name == "[DNS] noanswer.cname.local"
    assert monitor.status == MonitorStatus.ALERT
    assert monitor.external_link == ""

@mock.patch('dns.resolver.Resolver')
def test_process_custom_resolvers(mock_class):

  mock_instance = mock_class.return_value

  mock_instance.resolve.side_effect = dns_mock

  update_monitor_process("dns",
    configuration=dict(
      nameservers=['-1.-1.-1.-1'],
      port=53
    )
  )

  with app.app_context():
    monitor = get_resource(Monitor, MONITORS["a.local"])
    assert monitor.name == "[DNS] a.local"
    assert monitor.status == MonitorStatus.OK
    assert monitor.external_link == "ip://127.0.0.1"
