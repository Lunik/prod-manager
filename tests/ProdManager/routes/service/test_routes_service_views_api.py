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

class TestRoutesServiceViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
      app.token = pytest.helpers.generate_token(client, ["service_api"])
      app.ro_token = pytest.helpers.generate_token(client, [])

    return app

  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/api/service'):
      self.assertEqual(request.endpoint, 'service_api.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/api/service/1'):
      self.assertEqual(request.endpoint, 'service_api.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/api/service')
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_list_with_client_2(self, app):
    with app.test_client() as client:
      rv = client.get('/api/service?page=99999999999999999999')
      assert rv.status_code == 400

    with app.test_client() as client:
      rv = client.get('/api/service?per_page=99999999999999999999')
      assert rv.status_code == 400

  def test_show_with_client(self, app):
    service_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/api/service/create', data=dict(
        name=service_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{service_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client_2(self, app):
    service_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/service/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          name=service_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{service_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/api/service/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/api/service/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert re.match(r"http://localhost/api/service/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/service/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
      )
      assert b'"name": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post('/api/service/create',
        data=dict(
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/service/create',
        headers={
          "Authorization": f"Bearer {app.ro_token}"
        },
        data=dict(
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert b'"token": ["Token doesn\'t have enought permissions.' in rv.data
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_update_with_client(self, app):
    service_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    service_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/service/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
        name=service_name
      ))

      service_uri = rv.headers.get('Location')

      rv = client.post(f"{service_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          name=service_name_2
      ))

      assert re.match(r"http://localhost/api/service/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(service_uri)

      self.assertInResponse(f'"name": "{service_name_2}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{service_uri}/update",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
      )

      assert b'"name": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_delete_with_client(self, app):
    service_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/service/create',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
        data=dict(
          name=service_name
      ))

      service_uri = rv.headers.get('Location')

      rv = client.post(f"{service_uri}/delete",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
      )

      assert re.match(r"http://localhost/api/service", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/api/service/-1/delete",
        headers={
          "Authorization": f"Bearer {app.token}"
        },
      )

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
