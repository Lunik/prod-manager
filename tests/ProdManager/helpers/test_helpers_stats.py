import random
import string
import re
import flask_unittest
import pytest
import os

from ProdManager import create_app
from ProdManager.plugins import redis_client
from ProdManager.helpers.stats import get_resource_view

def test_resource_view_stat_disabled():
  app = create_app()
  app.config['STATS_ENABLED'] = False

  with app.app_context():
    assert get_resource_view() == None


TEST_REDIS_HOSTNAME = os.environ.get('TEST_REDIS_HOSTNAME', 'localhost')
TEST_REDIS_PORT = int(os.environ.get('TEST_REDIS_PORT', 6379))

class TestStatsResourceViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['STATS_ENABLED'] = True

    app.config['REDIS_URL'] = f"redis://{TEST_REDIS_HOSTNAME}:{TEST_REDIS_PORT}"
    redis_client.init_app(app)

    return app

  @pytest.mark.skipif(not pytest.helpers.redis_available(TEST_REDIS_HOSTNAME, TEST_REDIS_PORT), reason="No Redis instance found for tests")
  def test_show_with_client(self, app):
    scope_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/scope/create', data=dict(
        name=scope_name
      ))

      resource_location = rv.headers.get('Location')

      rv = client.get(resource_location)

      res = re.match(r'.*<div class="resource_view"><svg.*</svg>(\d+)', rv.data.decode('utf-8'))
      count = int(res.group(1))

      assert type(count) == int

      rv = client.get(resource_location)

      res = re.match(r'.*<div class="resource_view"><svg.*</svg>(\d+)', rv.data.decode('utf-8'))
      count_2 = int(res.group(1))

      assert count + 1 == count_2

class TestStatsResourceViewsRedisKO(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['STATS_ENABLED'] = True

    app.config['REDIS_URL'] = "redis://invalid"
    redis_client.init_app(app)
    
    return app

  def test_show_with_client(self, app):
    scope_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/scope/create', data=dict(
        name=scope_name
      ))

      resource_location = rv.headers.get('Location')

      rv = client.get(resource_location)

      res = re.match(r'.*<div class="resource_view"><svg.*</svg>(∞)', rv.data.decode('utf-8'))
      
      assert res.group(1) == "∞"