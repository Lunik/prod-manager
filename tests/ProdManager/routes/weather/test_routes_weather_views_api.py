import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app
from ProdManager.helpers.pagination import PAGINATION_MAX_PAGE, PAGINATION_MAX_PER_PAGE

class TestRoutesWeatherViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app(scheduled_jobs=False)
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_monitor_endpoint_with_app(self, app):
    with app.test_request_context('/api/weather/monitor'):
      self.assertEqual(request.endpoint, 'weather_api.monitor')

  def test_incident_endpoint_with_app(self, app):
    with app.test_request_context('/api/weather/incident'):
      self.assertEqual(request.endpoint, 'weather_api.incident')

  def test_maintenance_endpoint_with_app(self, app):
    with app.test_request_context('/api/weather/maintenance'):
      self.assertEqual(request.endpoint, 'weather_api.maintenance')

  def test_monitor_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/api/weather/monitor')
      self.assertInResponse(b'{', rv)
      self.assertInResponse(b'}', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_monitor_with_client_2(self, app):
    with app.test_client() as client:
      rv = client.get('/api/weather/monitor?scope=1')
      self.assertInResponse(b'{', rv)
      self.assertInResponse(b'}', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_incident_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/api/weather/incident')
      self.assertInResponse(b'{', rv)
      self.assertInResponse(b'}', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_incident_with_client_2(self, app):
    with app.test_client() as client:
      rv = client.get('/api/weather/incident?scope=1')
      self.assertInResponse(b'{', rv)
      self.assertInResponse(b'}', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_maintenance_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/api/weather/maintenance')
      self.assertInResponse(b'{', rv)
      self.assertInResponse(b'}', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_maintenance_with_client_2(self, app):
    with app.test_client() as client:
      rv = client.get('/api/weather/maintenance?scope=1')
      self.assertInResponse(b'{', rv)
      self.assertInResponse(b'}', rv)
      self.assertNotIn(b"__missing_translation", rv.data)
