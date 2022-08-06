import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app
from ProdManager.helpers.pagination import PAGINATION_MAX_PAGE, PAGINATION_MAX_PER_PAGE

class TestRoutesScopeViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/api/scope'):
      self.assertEqual(request.endpoint, 'scope_api.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/api/scope/1'):
      self.assertEqual(request.endpoint, 'scope_api.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/api/scope')
      self.assertInResponse(b'[{', rv)
      self.assertInResponse(b'}]', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_list_with_client_2(self, app):
    with app.test_client() as client:
      rv = client.get('/api/scope?page=99999999999999999999')
      assert rv.status_code == 400

    with app.test_client() as client:
      rv = client.get('/api/scope?per_page=99999999999999999999')
      assert rv.status_code == 400

  def test_show_with_client(self, app):
    scope_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/api/scope/create', data=dict(
        name=scope_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{scope_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client_2(self, app):
    scope_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/scope/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          name=scope_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'"name": "{scope_name}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/api/scope/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/api/scope/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert re.match(r"http://localhost/api/scope/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/scope/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        }
      )
      assert b'"name": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      rv = client.post('/api/scope/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          name=name
      ))
      assert re.match(r"http://localhost/api/scope/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post('/api/scope/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          name=name
      ))
      assert rv.status_code == 409
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/api/scope/create',
        data=dict(
          name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)


  def test_update_with_client(self, app):
    scope_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    scope_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/scope/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          name=scope_name
      ))

      scope_uri = rv.headers.get('Location')

      rv = client.post(f"{scope_uri}/update",
        data=dict(
          name=scope_name_2
      ))

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{scope_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          name=scope_name_2
      ))

      assert re.match(r"http://localhost/api/scope/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(scope_uri)

      self.assertInResponse(f'"name": "{scope_name_2}"'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{scope_uri}/update",
        headers={
          "APPLICATION-SECRET": "changeit"
        }
      )

      assert b'"name": ["This field is required."]' in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_delete_with_client(self, app):
    scope_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      rv = client.post('/api/scope/create',
        headers={
          "APPLICATION-SECRET": "changeit"
        },
        data=dict(
          name=scope_name
      ))

      scope_uri = rv.headers.get('Location')

      rv = client.post(f"{scope_uri}/delete")

      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{scope_uri}/delete",
        headers={
          "APPLICATION-SECRET": "changeit"
        }
      )

      assert re.match(r"http://localhost/api/scope", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/api/scope/-1/delete",
        headers={
          "APPLICATION-SECRET": "changeit"
        }
      )

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
