import random
import string
import re
from datetime import datetime
from urllib.parse import urljoin

import responses
import flask_unittest
import flask.globals
from flask import request, g

from ProdManager.helpers.openid import OpenID
from ProdManager import create_app

class TestRoutesAuthViews(flask_unittest.AppTestCase):

  @responses.activate
  def create_app(self):
    app = create_app(scheduled_jobs=False)
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['OPENID_ENABLED'] = True
    app.config['OPENID_DISCOVER_URL'] = "http://sso.example.local/realms/master/"
    app.config['OPENID_CLIENT_ID'] = "pytest"
    app.config['OPENID_CLIENT_SECRET'] = "super_secret"
    app.config["SERVER_NAME"] = "demo.local"

    from ProdManager.routes import openid
    app.register_blueprint(openid.view, url_prefix="/openid")

    openid = OpenID()

    responses.get(
      urljoin(app.config['OPENID_DISCOVER_URL'], ".well-known/openid-configuration"),
      json=dict(
        authorization_endpoint=urljoin(app.config['OPENID_DISCOVER_URL'], "protocol/openid-connect/auth"),
        token_endpoint=urljoin(app.config['OPENID_DISCOVER_URL'], "protocol/openid-connect/token")
      )
    )
    openid.init_app(app)

    return app


  def test_login_endpoint_with_app(self, app):
    with app.test_request_context('/openid/login'):
      self.assertEqual(request.endpoint, 'openid.login')

  def test_logout_endpoint_with_app(self, app):
    with app.test_request_context('/openid/callback'):
      self.assertEqual(request.endpoint, 'openid.callback')
