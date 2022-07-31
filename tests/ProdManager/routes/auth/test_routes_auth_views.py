import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app

class TestRoutesAuthViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_login_endpoint_with_app(self, app):
    with app.test_request_context('/login'):
      self.assertEqual(request.endpoint, 'auth.login')

  def test_logout_endpoint_with_app(self, app):
    with app.test_request_context('/logout'):
      self.assertEqual(request.endpoint, 'auth.logout')

  def test_login_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/login')
      self.assertInResponse(b'<h1 id="title">Login</h1>', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_do_login_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/login', data=dict(secret="changeit"))

      assert re.match(r"http://localhost/", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/login')
      assert b"secret : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/login', data=dict(secret="invalid"))
      assert b"secret : Invalid secret" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/login', data=dict(secret="changeit", remember_me=True))

      assert re.match(r"http://localhost/", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_logout_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/logout')
      assert re.match(r"http://localhost/", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/logout')
      assert re.match(r"http://localhost/", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_logged_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/login', data=dict(secret="changeit"))
      rv = client.get('/logged')
      assert b"True" in rv.data

    with app.test_client() as client:
      rv = client.get('/logged')
      assert b"False" in rv.data