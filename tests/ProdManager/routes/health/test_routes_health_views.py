import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app

class TestRoutesHealthViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_login_endpoint_with_app(self, app):
    with app.test_request_context('/health'):
      self.assertEqual(request.endpoint, 'health.probe')

  def test_login_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/health')
      self.assertInResponse(b'OK', rv)
