import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app

class TestRoutesMonitorViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app(scheduled_jobs=False)
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/monitor'):
      self.assertEqual(request.endpoint, 'monitor.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/monitor/1'):
      self.assertEqual(request.endpoint, 'monitor.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/monitor')
      self.assertInResponse(b'<h1>Monitors list</h1>', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/monitor/create', data=dict(
        scope="1",
        service="1",
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert re.match(r"http://localhost/monitor/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/monitor/create', data=dict(
        scope="1",
        service="1",
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        integration="pytest",
        external_reference="0000000000",
        external_link="https://example.org"
      ))
      assert re.match(r"http://localhost/monitor/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/monitor/create', data=dict(
        service="1",
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert b"scope : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/monitor/create', data=dict(
        service="1",
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client(self, app):
    monitor_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/monitor/create', data=dict(
        scope="1",
        service="1",
        name=monitor_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'<h1 id="title">Monitor - {monitor_name}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/monitor/create', data=dict(
        scope="1",
        service="1",
        name=monitor_name,
        integration="pytest",
        external_reference="0000000000",
        external_link="https://example.org"
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'pytest'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/monitor/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_update_with_client(self, app):
    monitor_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    monitor_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/monitor/create', data=dict(
        scope="1",
        service="1",
        name=monitor_name
      ))

      monitor_uri = rv.headers.get('Location')

      rv = client.post(f"{monitor_uri}/update", data=dict(
        scope="1",
        service="1",
        status="ok",
        name=monitor_name_2,
        external_reference="0000000000",
        external_link="https://example.org"
      ))

      assert re.match(r"http://localhost/monitor/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(monitor_uri)

      self.assertInResponse(f'<h1 id="title">Monitor - {monitor_name_2}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{monitor_uri}/update", data=dict(
        scope="1",
        service="1",
        name=monitor_name_2
      ))

      assert b"status : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{monitor_uri}/update", data=dict(
        scope="1",
        service="1",
        status="warning",
        name=monitor_name_2
      ))

      rv = client.get(monitor_uri)

      self.assertInResponse(b'WARNING', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{monitor_uri}/update", data=dict(
        scope="1",
        service="1",
        status="alert",
        name=monitor_name_2
      ))

      rv = client.get(monitor_uri)

      self.assertInResponse(b'ALERT', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_delete_with_client(self, app):
    monitor_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/monitor/create', data=dict(
        scope="1",
        service="1",
        name=monitor_name
      ))

      monitor_uri = rv.headers.get('Location')

      rv = client.post(f"{monitor_uri}/delete")

      assert re.match(r"http://localhost/monitor", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/monitor/-1/delete")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
