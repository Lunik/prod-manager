import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app
from ProdManager.helpers.pagination import PAGINATION_MAX_PAGE, PAGINATION_MAX_PER_PAGE

class TestRoutesMonitorViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/api/monitor'):
      self.assertEqual(request.endpoint, 'monitor_api.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/api/monitor/1'):
      self.assertEqual(request.endpoint, 'monitor_api.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/api/monitor')
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_list_with_client_2(self, app):
    with app.test_client() as client:
      rv = client.get('/api/monitor?page=99999999999999999999')
      assert rv.status_code == 400

    with app.test_client() as client:
      rv = client.get('/api/monitor?per_page=99999999999999999999')
      assert rv.status_code == 400

  def test_show_with_client(self, app):
    monitor_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/api/monitor/create', data=dict(
        scope="1",
        service="1",
        name=monitor_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{monitor_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client_2(self, app):
    monitor_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/monitor/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          name=monitor_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{monitor_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/api/monitor/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get('/api/monitor?scope=1')
      self.assertInResponse(f'"name": "{monitor_name}"'.encode(), rv)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)

      rv = client.get('/api/monitor?scope=2')
      self.assertNotIn(f'"name": "{monitor_name}"'.encode(), rv.data)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)


  def test_create_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/api/monitor/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert re.match(r"http://localhost/api/monitor/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/monitor/create',
        data=dict(
          scope="1",
          service="1",
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/monitor/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          service="1",
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert b'"scope": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)


  def test_update_with_client(self, app):
    monitor_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    monitor_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/monitor/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          name=monitor_name
      ))

      monitor_uri = rv.headers.get('Location')

      rv = client.post(f"{monitor_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          status="ok",
          name=monitor_name_2
      ))

      assert re.match(r"http://localhost/api/monitor/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{monitor_uri}/update",
        data=dict(
          scope="1",
          service="1",
          status="ok",
          name=monitor_name_2
      ))

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(monitor_uri)

      self.assertInResponse(f'"name": "{monitor_name_2}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{monitor_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          name=monitor_name_2
      ))

      assert b'"status": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{monitor_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          status="warning",
          name=monitor_name_2
      ))

      rv = client.get(monitor_uri)

      self.assertInResponse(b'warning', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{monitor_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          status="alert",
          name=monitor_name_2
      ))

      rv = client.get(monitor_uri)

      self.assertInResponse(b'alert', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_delete_with_client(self, app):
    monitor_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/monitor/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          scope="1",
          service="1",
          name=monitor_name
      ))

      monitor_uri = rv.headers.get('Location')

      rv = client.post(f"{monitor_uri}/delete")

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{monitor_uri}/delete",
        headers={
          "APPLICATION-SECRET": "changeit"
        }
      )

      assert re.match(r"http://localhost/api/monitor", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/api/monitor/-1/delete",
        headers={
          "APPLICATION-SECRET": "changeit"
        }
      )

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
