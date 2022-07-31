import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app

class TestRoutesScopeViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/scope'):
      self.assertEqual(request.endpoint, 'scope.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/scope/1'):
      self.assertEqual(request.endpoint, 'scope.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/scope')
      self.assertInResponse(b'<h1>Scopes list</h1>', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/scope/create', data=dict(
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert re.match(r"http://localhost/scope/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/scope/create')
      assert b"name : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/scope/create', data=dict(
        name=name
      ))
      assert re.match(r"http://localhost/scope/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post('/scope/create', data=dict(
        name=name
      ))
      assert rv.status_code == 409
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/scope/create', data=dict(
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client(self, app):
    scope_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/scope/create', data=dict(
        name=scope_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'<h1 id="title">Scope - {scope_name}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/scope/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_update_with_client(self, app):
    scope_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    scope_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/scope/create', data=dict(
        name=scope_name
      ))

      scope_uri = rv.headers.get('Location')

      rv = client.post(f"{scope_uri}/update", data=dict(
        name=scope_name_2
      ))

      assert re.match(r"http://localhost/scope/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(scope_uri)

      self.assertInResponse(f'<h1 id="title">Scope - {scope_name_2}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{scope_uri}/update")

      assert b"name : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_delete_with_client(self, app):
    scope_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/scope/create', data=dict(
        name=scope_name
      ))

      scope_uri = rv.headers.get('Location')

      rv = client.post(f"{scope_uri}/delete")

      assert re.match(r"http://localhost/scope", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/scope/-1/delete")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
