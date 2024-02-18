import random
import string
import re
from datetime import datetime
from packaging.version import parse as parse_version

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app, __version__

class TestRoutesHealthViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app(scheduled_jobs=False)
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_login_endpoint_with_app(self, app):
    with app.test_request_context('/health'):
      self.assertEqual(request.endpoint, 'health.probe')

  def test_login_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/health')
      self.assertInResponse(b'OK', rv)

  def test_login_endpoint_with_app(self, app):
    with app.test_request_context('/health/version'):
      self.assertEqual(request.endpoint, 'health.version')

  def test_login_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/health/version')
      self.assertInResponse(parse_version(__version__).base_version.encode('UTF-8'), rv)
