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

class TestRoutesAnnouncementViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app(scheduled_jobs=False)
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
      app.token = pytest.helpers.generate_token(client, ["announcement_api"])
      app.ro_token = pytest.helpers.generate_token(client, [])

    return app

  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/api/announcement'):
      self.assertEqual(request.endpoint, 'announcement_api.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/api/announcement/1'):
      self.assertEqual(request.endpoint, 'announcement_api.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/api/announcement')
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_list_with_client_2(self, app):
    with app.test_client() as client:
      rv = client.get('/api/announcement?page=99999999999999999999')
      assert rv.status_code == 400

    with app.test_client() as client:
      rv = client.get('/api/announcement?per_page=99999999999999999999')
      assert rv.status_code == 400

  def test_show_with_client(self, app):
    announcement_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/api/announcement/create', data=dict(
        scope="1",
        service="1",
        level="low",
        start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=announcement_name,
        description="placeholder"
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{announcement_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client_2(self, app):
    announcement_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/announcement/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          level="low",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=announcement_name,
        description="placeholder"
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{announcement_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/api/announcement/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get('/api/announcement?service_status=up')
      self.assertInResponse(f'"name": "{announcement_name}"'.encode(), rv)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)

      rv = client.get(f"/api/announcement?start_before={datetime.now().strftime('%Y-%m-%d %H:%M')}")
      self.assertNotIn(f'"name": "{announcement_name}"'.encode(), rv.data)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)

      rv = client.get(f"/api/announcement?start_after={datetime.now().strftime('%Y-%m-%d %H:%M')}")
      self.assertInResponse(f'"name": "{announcement_name}"'.encode(), rv)
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/api/announcement/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          level="low",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
          description="placeholder"
      ))
      assert re.match(r"http://localhost/api/announcement/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/announcement/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          service="1",
          level="low",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
          description="placeholder"
      ))
      assert b'"scope": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/announcement/create',
        data=dict(
          service="1",
          level="low",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
          description="placeholder"
      ))
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/announcement/create',
        headers={
          "Authorization": f"Bearer {app.ro_token}"
        },
        data=dict(
          scope="1",
          service="1",
          level="low",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
          description="placeholder"
      ))
      assert b'"token": ["Token doesn\'t have enought permissions.' in rv.data
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_update_with_client(self, app):
    announcement_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    announcement_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/announcement/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          level="low",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=announcement_name,
          description="placeholder"
      ))

      announcement_uri = rv.headers.get('Location')

      rv = client.post(f"{announcement_uri}/update",
        data=dict(
          scope="1",
          service="1",
          level="low",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=announcement_name_2,
          description="placeholder"
      ))

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{announcement_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          level="low",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=announcement_name_2,
          description="placeholder"
      ))

      assert re.match(r"http://localhost/api/announcement/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(announcement_uri)

      self.assertInResponse(f'"name": "{announcement_name_2}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{announcement_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=announcement_name_2,
          description="placeholder"
      ))

      assert b'"level": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{announcement_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          level="high",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=announcement_name_2,
          description="placeholder"
      ))

      rv = client.get(announcement_uri)

      self.assertInResponse(b'high', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_delete_with_client(self, app):
    announcement_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/announcement/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          scope="1",
          service="1",
          level="high",
          start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
          name=announcement_name,
          description="placeholder"
      ))

      announcement_uri = rv.headers.get('Location')

      rv = client.post(f"{announcement_uri}/delete")

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{announcement_uri}/delete",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
      )

      assert re.match(r"http://localhost/api/announcement", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/api/announcement/-1/delete")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
