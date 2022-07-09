import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app

class TestRoutesIncidentViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/incident'):
      self.assertEqual(request.endpoint, 'incident.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/incident/1'):
      self.assertEqual(request.endpoint, 'incident.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/incident')
      self.assertInResponse(b'<h1>Incidents list</h1>', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/incident/create', data=dict(
        scope="1",
        service="1",
        severity="moderate",
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert re.match(r"/incident/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/incident/create', data=dict(
        service="1",
        severity="moderate",
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert b"scope : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client(self, app):
    incident_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/incident/create', data=dict(
        scope="1",
        service="1",
        severity="moderate",
        name=incident_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'<h1 id="title">Incident - {incident_name}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/incident/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_update_with_client(self, app):
    incident_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    incident_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/incident/create', data=dict(
        scope="1",
        service="1",
        severity="moderate",
        external_reference="INC0000123",
        name=incident_name
      ))
      self.assertNotIn(b"__missing_translation", rv.data)

      incident_uri = rv.headers.get('Location')

      rv = client.post(f"{incident_uri}/update", data=dict(
        scope="1",
        service="1",
        severity="moderate",
        status="active",
        name=incident_name_2,
        external_reference="INC0000123",
        start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      assert re.match(r"/incident/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(incident_uri)

      self.assertInResponse(f'<h1 id="title">Incident - {incident_name_2}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/update", data=dict(
        scope="1",
        service="1",
        severity="moderate",
        name=incident_name_2,
        start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      assert b"status : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/update", data=dict(
        scope="1",
        service="1",
        severity="moderate",
        status="investigating",
        name=incident_name_2,
        start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      rv = client.get(incident_uri)

      self.assertInResponse(b'INVESTIGATING', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/update", data=dict(
        scope="1",
        service="1",
        severity="moderate",
        status="stable",
        name=incident_name_2,
        start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      rv = client.get(incident_uri)

      self.assertInResponse(b'STABLE', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/update", data=dict(
        scope="1",
        service="1",
        severity="moderate",
        status="resolved",
        name=incident_name_2,
        start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      rv = client.get(incident_uri)

      self.assertInResponse(b'RESOLVED', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_comment_with_client(self, app):
    incident_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/incident/create', data=dict(
        scope="1",
        service="1",
        severity="moderate",
        name=incident_name,
        start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      incident_uri = rv.headers.get('Location')

      rv = client.post(f"{incident_uri}/comment", data=dict(
        comment="THIS_IS_A_TEST",
      ))

      assert re.match(r"/incident/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/comment")

      assert b"comment : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(incident_uri)
      self.assertInResponse(b'THIS_IS_A_TEST', rv)

  def test_delete_with_client(self, app):
    incident_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/incident/create', data=dict(
        scope="1",
        service="1",
        severity="moderate",
        name=incident_name,
        start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      incident_uri = rv.headers.get('Location')

      rv = client.post(f"{incident_uri}/delete")

      assert re.match(r"/incident", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/incident/-1/delete")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
