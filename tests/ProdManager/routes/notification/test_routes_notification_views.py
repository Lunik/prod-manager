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
    app.config['MAIL_ENABLED'] = True
    return app


  def test_notification_endpoint_with_app(self, app):
    with app.test_request_context('/notification'):
      self.assertEqual(request.endpoint, 'notification.index')

  def test_notification_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/notification')
      self.assertInResponse(b'<h1 id="title">Subscribe to notifications</h1>', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_subscribe_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/notification/suscribe', data=dict(email="test@exemple.org"))
      assert b"Successfully+subscribed" in rv.data
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/notification/suscribe', data=dict(email="test@exemple"))
      assert b"email : Invalid email address" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/notification/suscribe')
      assert b"email : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_unsubscribe_with_client(self, app):
    with app.test_client() as client:
      rv = client.post('/notification/unsuscribe', data=dict(email="test@exemple.org"))
      assert b"Successfully+unsubscribed" in rv.data
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/notification/unsuscribe', data=dict(email="test@exemple"))
      assert b"email : Invalid email address" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/notification/unsuscribe')
      assert b"email : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)