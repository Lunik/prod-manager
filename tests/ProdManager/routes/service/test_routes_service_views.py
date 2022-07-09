import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app

class TestRoutesServiceViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/service'):
      self.assertEqual(request.endpoint, 'service.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/service/1'):
      self.assertEqual(request.endpoint, 'service.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/service')
      self.assertInResponse(b'<h1>Services list</h1>', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/service/create', data=dict(
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
      ))
      assert re.match(r"/service/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/service/create')
      assert b"name : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client(self, app):
    service_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/service/create', data=dict(
        name=service_name
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'<h1 id="title">Service - {service_name}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/service/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_update_with_client(self, app):
    service_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    service_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/service/create', data=dict(
        name=service_name
      ))

      service_uri = rv.headers.get('Location')

      rv = client.post(f"{service_uri}/update", data=dict(
        name=service_name_2
      ))

      assert re.match(r"/service/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(service_uri)

      self.assertInResponse(f'<h1 id="title">Service - {service_name_2}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{service_uri}/update")

      assert b"name : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_delete_with_client(self, app):
    service_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/service/create', data=dict(
        name=service_name
      ))

      service_uri = rv.headers.get('Location')

      rv = client.post(f"{service_uri}/delete")

      assert re.match(r"/service", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/service/-1/delete")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
