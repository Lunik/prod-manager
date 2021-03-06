import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app

class TestRoutesRootViews(flask_unittest.AppTestCase):

  def create_app(self):
    return create_app()

  def test_index_endpoint_with_app(self, app):
    with app.test_request_context('/'):
      self.assertEqual(request.endpoint, 'root.index')

  def test_about_endpoint_with_app(self, app):
    with app.test_request_context('/about'):
      self.assertEqual(request.endpoint, 'root.about')

  def test_index_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/')
      self.assertInResponse(b'<h1 id="title">Dashboard</h1>', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_about_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/about')
      self.assertInResponse(b'<h1 id="title">About ProdManager</h1>', rv)
      self.assertNotIn(b"__missing_translation", rv.data)
