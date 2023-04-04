import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app

class TestRoutesMaintenanceViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app(scheduled_jobs=False)
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/maintenance'):
      self.assertEqual(request.endpoint, 'maintenance.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/maintenance/1'):
      self.assertEqual(request.endpoint, 'maintenance.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/maintenance')
      self.assertInResponse(b'<h1>Maintenances list</h1>', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/maintenance/create', data=dict(
        scope="1",
        service="1",
        service_status="up",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert re.match(r"http://localhost/maintenance/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/maintenance/create', data=dict(
        service="1",
        service_status="up",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert b"scope : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/maintenance/create', data=dict(
        service="1",
        service_status="up",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/maintenance/create', data=dict(
        scope="1",
        service="1",
        service_status="up",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'<h1 id="title">Maintenance - {maintenance_name}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/maintenance/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_calendar_with_client(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/maintenance/create', data=dict(
        scope="1",
        service="1",
        service_status="up",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name
      ))

      rv = client.get(rv.headers.get('Location') + "/calendar")

      assert rv.status_code == 200
      assert rv.headers['Content-Type'] == "application/ics"
      assert rv.headers['Content-Disposition'] == f"attachment; filename={maintenance_name}.ics"
      self.assertInResponse(b'BEGIN:VCALENDAR', rv)
      self.assertInResponse(b'BEGIN:VEVENT', rv)

  def test_calendar_with_client_2(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/maintenance/create', data=dict(
        scope="1",
        service="1",
        service_status="up",
        external_reference="CHG000000",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name
      ))

      rv = client.get(rv.headers.get('Location') + "/calendar")

      assert rv.status_code == 200
      assert rv.headers['Content-Type'] == "application/ics"
      assert rv.headers['Content-Disposition'] == f"attachment; filename={maintenance_name}.ics"
      self.assertInResponse(b'BEGIN:VCALENDAR', rv)
      self.assertInResponse(b'BEGIN:VEVENT', rv)
      self.assertInResponse(b'SUMMARY:[CHG000000]', rv)

  def test_update_with_client(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    maintenance_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/maintenance/create', data=dict(
        scope="1",
        service="1",
        service_status="up",
        external_reference="CHG0000123",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name
      ))

      maintenance_uri = rv.headers.get('Location')

      rv = client.post(f"{maintenance_uri}/update", data=dict(
        scope="1",
        service="1",
        service_status="up",
        status="scheduled",
        external_reference="CHG0000123",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name_2
      ))

      assert re.match(r"http://localhost/maintenance/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(maintenance_uri)

      self.assertInResponse(f'<h1 id="title">Maintenance - {maintenance_name_2}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update", data=dict(
        scope="1",
        service="1",
        service_status="up",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name_2
      ))

      assert b"status : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update", data=dict(
        scope="1",
        service="1",
        service_status="up",
        status="in-progress",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name_2
      ))

      rv = client.get(maintenance_uri)

      self.assertInResponse(b'IN_PROGRESS', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update", data=dict(
        scope="1",
        service="1",
        service_status="up",
        status="succeed",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name_2
      ))

      rv = client.get(maintenance_uri)

      self.assertInResponse(b'SUCCEED', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update", data=dict(
        scope="1",
        service="1",
        service_status="up",
        status="failed",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name_2
      ))

      rv = client.get(maintenance_uri)

      self.assertInResponse(b'FAILED', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update", data=dict(
        scope="1",
        service="1",
        service_status="up",
        status="canceled",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name_2
      ))

      rv = client.get(maintenance_uri)

      self.assertInResponse(b'CANCELED', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_comment_with_client(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/maintenance/create', data=dict(
        scope="1",
        service="1",
        service_status="up",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name
      ))

      maintenance_uri = rv.headers.get('Location')

      rv = client.post(f"{maintenance_uri}/comment", data=dict(
        comment="THIS_IS_A_TEST",
      ))

      assert re.match(r"http://localhost/maintenance/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/comment")

      assert b"comment : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(maintenance_uri)
      self.assertInResponse(b'THIS_IS_A_TEST', rv)

  def test_delete_with_client(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/maintenance/create', data=dict(
        scope="1",
        service="1",
        service_status="up",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name
      ))

      maintenance_uri = rv.headers.get('Location')

      rv = client.post(f"{maintenance_uri}/delete")

      assert re.match(r"http://localhost/maintenance", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/maintenance/-1/delete")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
