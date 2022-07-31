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
    with app.test_request_context('/api/incident'):
      self.assertEqual(request.endpoint, 'incident_api.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/api/incident/1'):
      self.assertEqual(request.endpoint, 'incident_api.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/api/incident')
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/api/incident/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert re.match(r"http://localhost/api/incident/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/incident/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          service="1",
          severity="moderate",
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert b'"scope": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/incident/create',
        data=dict(
          service="1",
          severity="moderate",
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client(self, app):
    incident_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/api/incident/create', data=dict(
        scope="1",
        service="1",
        severity="moderate",
        name=incident_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{incident_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client_2(self, app):
    incident_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/incident/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          name=incident_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{incident_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/api/incident/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get('/api/incident?severity=moderate')
      self.assertInResponse(f'"name": "{incident_name}"'.encode(), rv)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)

      rv = client.get(f"/api/incident?impact_before={datetime.now().strftime('%Y-%m-%d %H:%M')}")
      self.assertNotIn(f'"name": "{incident_name}"'.encode(), rv.data)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)

      rv = client.get(f"/api/incident?impact_after={datetime.now().strftime('%Y-%m-%d %H:%M')}")
      self.assertInResponse(f'"name": "{incident_name}"'.encode(), rv)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)

  def test_update_with_client(self, app):
    incident_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    incident_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/incident/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          external_reference="INC0000123",
          name=incident_name
      ))
      self.assertNotIn(b"__missing_translation", rv.data)

      incident_uri = rv.headers.get('Location')

      rv = client.post(f"{incident_uri}/update",
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          status="active",
          name=incident_name_2,
          external_reference="INC0000123",
          start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          status="active",
          name=incident_name_2,
          external_reference="INC0000123",
          start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      assert re.match(r"http://localhost/api/incident/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(incident_uri)

      self.assertInResponse(f'"name": "{incident_name_2}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          name=incident_name_2,
          start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      assert b'"status": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          status="investigating",
          name=incident_name_2,
          start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      rv = client.get(incident_uri)

      self.assertInResponse(b'investigating', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          status="stable",
          name=incident_name_2,
          start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      rv = client.get(incident_uri)

      self.assertInResponse(b'stable', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          status="resolved",
          name=incident_name_2,
          start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      rv = client.get(incident_uri)

      self.assertInResponse(b'resolved', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_comment_with_client(self, app):
    incident_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/incident/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          name=incident_name,
          start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      incident_uri = rv.headers.get('Location')

      rv = client.post(f"{incident_uri}/comment",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          comment="THIS_IS_A_TEST",
      ))

      assert re.match(r"http://localhost/api/incident/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(incident_uri,
        headers={
          "APPLICATION-SECRET": "changeit"
        }
      )
      self.assertInResponse(b'THIS_IS_A_TEST', rv)

      rv = client.post(f"{incident_uri}/comment",
        headers={
          "APPLICATION-SECRET": "changeit"
        }
      )

      assert b'"comment": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/comment")

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_delete_with_client(self, app):
    incident_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/incident/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          severity="moderate",
          name=incident_name,
          start_impact_date=datetime.now().strftime('%Y-%m-%dT%H:%M')
      ))

      incident_uri = rv.headers.get('Location')

      rv = client.post(f"{incident_uri}/delete")

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{incident_uri}/delete",
        headers={
          "APPLICATION-SECRET": "changeit"
        }
      )

      assert re.match(r"http://localhost/api/incident", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/api/incident/-1/delete",
        headers={
          "APPLICATION-SECRET": "changeit"
        }
      )

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
