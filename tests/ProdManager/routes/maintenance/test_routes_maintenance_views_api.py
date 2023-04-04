import random
import string
import re
from datetime import datetime
import pytest

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app
from ProdManager.helpers.pagination import PAGINATION_MAX_PAGE, PAGINATION_MAX_PER_PAGE

class TestRoutesMaintenanceViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app(scheduled_jobs=False)
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
      app.token = pytest.helpers.generate_token(client, ["maintenance_api"])
      app.ro_token = pytest.helpers.generate_token(client, [])

    return app

  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/api/maintenance'):
      self.assertEqual(request.endpoint, 'maintenance_api.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/api/maintenance/1'):
      self.assertEqual(request.endpoint, 'maintenance_api.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/api/maintenance')
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_list_with_client_2(self, app):
    with app.test_client() as client:
      rv = client.get('/api/maintenance?page=99999999999999999999')
      assert rv.status_code == 400

    with app.test_client() as client:
      rv = client.get('/api/maintenance?per_page=99999999999999999999')
      assert rv.status_code == 400

  def test_show_with_client(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/api/maintenance/create', data=dict(
        scope="1",
        service="1",
        service_status="up",
        scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=maintenance_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{maintenance_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client_2(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/maintenance/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{maintenance_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/api/maintenance/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get('/api/maintenance?service_status=up')
      self.assertInResponse(f'"name": "{maintenance_name}"'.encode(), rv)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)

      rv = client.get(f"/api/maintenance?start_before={datetime.now().strftime('%Y-%m-%d %H:%M')}")
      self.assertNotIn(f'"name": "{maintenance_name}"'.encode(), rv.data)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)

      rv = client.get(f"/api/maintenance?start_after={datetime.now().strftime('%Y-%m-%d %H:%M')}")
      self.assertInResponse(f'"name": "{maintenance_name}"'.encode(), rv)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/api/maintenance/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert re.match(r"http://localhost/api/maintenance/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/maintenance/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          service="1",
          service_status="up",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert b'"scope": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/maintenance/create',
        data=dict(
          service="1",
          service_status="up",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/maintenance/create',
        headers={
          "Authorization": f"Bearer {app.ro_token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert b'"token": ["Token doesn\'t have enought permissions.' in rv.data
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_calendar_with_client(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/maintenance/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
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

  def test_update_with_client(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    maintenance_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/maintenance/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          external_reference="CHG0000123",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name
      ))

      maintenance_uri = rv.headers.get('Location')

      rv = client.post(f"{maintenance_uri}/update",
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          status="scheduled",
          external_reference="CHG0000123",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name_2
      ))

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          status="scheduled",
          external_reference="CHG0000123",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name_2
      ))

      assert re.match(r"http://localhost/api/maintenance/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(maintenance_uri)

      self.assertInResponse(f'"name": "{maintenance_name_2}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name_2
      ))

      assert b'"status": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          status="in-progress",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name_2
      ))

      rv = client.get(maintenance_uri)

      self.assertInResponse(b'in-progress', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          status="succeed",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name_2
      ))

      rv = client.get(maintenance_uri)

      self.assertInResponse(b'succeed', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          status="failed",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name_2
      ))

      rv = client.get(maintenance_uri)

      self.assertInResponse(b'failed', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          status="canceled",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name_2
      ))

      rv = client.get(maintenance_uri)

      self.assertInResponse(b'canceled', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_comment_with_client(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/maintenance/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name
      ))

      maintenance_uri = rv.headers.get('Location')

      rv = client.post(f"{maintenance_uri}/comment",
        data=dict(
          comment="THIS_IS_A_TEST",
      ))

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/comment",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          comment="THIS_IS_A_TEST",
      ))

      assert re.match(r"http://localhost/api/maintenance/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/comment",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
      )

      assert b'"comment": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(maintenance_uri,
        headers={
          "Authorization": f"Bearer {app.token}"
        },
      )
      self.assertInResponse(b'THIS_IS_A_TEST', rv)

  def test_delete_with_client(self, app):
    maintenance_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/maintenance/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          service_status="up",
          scheduled_start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          scheduled_end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=maintenance_name
      ))

      maintenance_uri = rv.headers.get('Location')

      rv = client.post(f"{maintenance_uri}/delete")

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{maintenance_uri}/delete",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
      )

      assert re.match(r"http://localhost/api/maintenance", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/api/maintenance/-1/delete")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
