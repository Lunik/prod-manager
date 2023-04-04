import random
import string
import re
import os
from datetime import datetime
import pytest
from unittest import mock
from unittest.mock import MagicMock

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app
from ProdManager.helpers.pagination import PAGINATION_MAX_PAGE, PAGINATION_MAX_PER_PAGE

from ProdManager.plugins import redis_client

class TestAPIRateLimitNoRedis(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app(scheduled_jobs=False)
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['API_RATELIMIT_ENABLED'] = True

    app.config['REDIS_URL'] = "redis://invalid"
    redis_client.init_app(app)

    with app.test_client() as client:
      app.ro_token = pytest.helpers.generate_token(client, [])

    return app

  def test_api_ratelimit_with_no_auth(self, app):
    with app.test_client() as client:
      rv = client.get('/api/scope')
      assert rv.status_code == 200

  def test_api_ratelimit_with_session(self, app):
    with app.test_client() as client:
      rv = client.post('/login', data=dict(secret="changeit"))
      assert rv.status_code == 302
      rv = client.get('/api/scope')
      assert rv.status_code == 200

  def test_api_ratelimit_with_token(self, app):
    with app.test_client() as client:
      rv = client.get('/api/scope',
        headers={
          "Authorization": f"Bearer {app.ro_token}"
        }
      )
      assert rv.status_code == 200

TEST_REDIS_HOSTNAME = os.environ.get('TEST_REDIS_HOSTNAME', 'localhost')
TEST_REDIS_PORT = int(os.environ.get('TEST_REDIS_PORT', 6379))

@pytest.mark.skipif(not pytest.helpers.redis_available(TEST_REDIS_HOSTNAME, TEST_REDIS_PORT), reason="No Redis instance found for tests")
class TestAPIRateLimitWithRedis(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app(scheduled_jobs=False)
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['API_RATELIMIT_ENABLED'] = True
    app.config['API_RATELIMIT_DEFAULT'] = 5
    app.config['API_RATELIMIT_LOGGED'] = 10

    app.config['REDIS_URL'] = f"redis://{TEST_REDIS_HOSTNAME}:{TEST_REDIS_PORT}"
    redis_client.init_app(app)

    redis_client.flushdb()

    with app.test_client() as client:
      app.ro_token = pytest.helpers.generate_token(client, [])

    return app

  @pytest.mark.order(1)
  def test_api_ratelimit_with_no_auth(self, app):
    with app.test_client() as client:
      rv = client.get('/api/scope')
      assert rv.status_code == 200

  @pytest.mark.order(2)
  def test_api_ratelimit_with_no_auth_overflow(self, app):
    with app.test_client() as client:
      for i in range(0, app.config['API_RATELIMIT_DEFAULT']):
        client.get('/api/scope')

      rv = client.get('/api/scope')
      assert rv.status_code == 429
      assert int(rv.headers.get('Retry-After')) > 0


  @pytest.mark.order(3)
  def test_api_ratelimit_with_session(self, app):
    with app.test_client() as client:
      rv = client.post('/login', data=dict(secret="changeit"))
      assert rv.status_code == 302
      rv = client.get('/api/scope')
      assert rv.status_code == 200

  @pytest.mark.order(4)
  def test_api_ratelimit_with_session_overflow(self, app):
    with app.test_client() as client:
      rv = client.post('/login', data=dict(secret="changeit"))
      assert rv.status_code == 302

      for i in range(0, app.config['API_RATELIMIT_LOGGED']):
        client.get('/api/scope')

      rv = client.get('/api/scope')
      assert rv.status_code == 429
      assert int(rv.headers.get('Retry-After')) > 0


  @pytest.mark.order(5)
  def test_api_ratelimit_with_token(self, app):
    with app.test_client() as client:
      rv = client.get('/api/scope',
        headers={
          "Authorization": f"Bearer {app.ro_token}"
        }
      )
      assert rv.status_code == 200

  @pytest.mark.order(6)
  def test_api_ratelimit_with_token_overflow(self, app):
    with app.test_client() as client:
      for i in range(0, app.config['API_RATELIMIT_LOGGED']):
        client.get('/api/scope',
          headers={
            "Authorization": f"Bearer {app.ro_token}"
          }
        )

      rv = client.get('/api/scope',
        headers={
          "Authorization": f"Bearer {app.ro_token}"
        }
      )
      assert rv.status_code == 429
      assert int(rv.headers.get('Retry-After')) > 0