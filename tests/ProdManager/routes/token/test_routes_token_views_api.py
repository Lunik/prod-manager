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
from ProdManager.helpers.auth import verify_jwt

class TestRoutesTokenViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
      app.token = pytest.helpers.generate_token(client)

    return app

  def test_create_endpoint_with_app(self, app):
    with app.test_request_context('/api/token/create'):
      self.assertEqual(request.endpoint, 'token_api.create')

  def test_create_endpoint_with_app(self, app):
    with app.test_request_context('/api/token/whoami'):
      self.assertEqual(request.endpoint, 'token_api.whoami')

  def test_create_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/api/token/create',
        data=dict(
          secret="changeit",
          name="pytest-unittest",
          description="Token only used for unittests",
          permissions=[],
      ))
      assert rv.status_code == 200
      self.assertNotIn(b"__missing_translation", rv.data)

      verify_jwt(rv.data.decode('utf-8').replace('"', ''))

      rv = client.post('/api/token/create',
        data=dict(
          name="pytest-unittest",
          description="Token only used for unittests",
          permissions=[],
      ))
      assert rv.status_code == 400
      assert b'"secret": ["This field is required."]' in rv.data
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post('/api/token/create',
        data=dict(
          secret="invalid-value",
          name="pytest-unittest",
          description="Token only used for unittests",
          permissions=[],
      ))
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_whoami_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/api/token/whoami',
        headers={
          "Authorization": f"Bearer {app.token}"
        },
      )
      assert rv.status_code == 200
      self.assertNotIn(b"__missing_translation", rv.data)

      assert b'"aud": "pytest-unittest"' in rv.data

    with app.test_client() as client:
      rv = client.get('/api/token/whoami',
        headers={
          "Authorization": f"Bearer {app.token[:-1]}"
        },
      )
      assert rv.status_code == 401
      assert b'"token": ["Signature verification failed"]' in rv.data
      self.assertNotIn(b"__missing_translation", rv.data)


    with app.test_client() as client:
      rv = client.get('/api/token/whoami',
        headers={
          "Authorization": f"{app.token}"
        },
      )
      assert rv.status_code == 401
      assert b'"token": ["Token has not the right format or type.' in rv.data
      self.assertNotIn(b"__missing_translation", rv.data)
