import logging
from urllib.parse import urlencode, urljoin

import requests
import jwt

from ProdManager.helpers.links import custom_url_for

class OpenID():
  logger = logging.getLogger('gunicorn.error')
  discover_url = None
  client_id = None
  client_secret = None
  client_scopes = []
  allowed_role = None
  roles_attribute = None
  metadata = dict()

  def init_app(self, flask_app):
    self.discover_url = flask_app.config.get('OPENID_DISCOVER_URL')
    self.client_id = flask_app.config.get('OPENID_CLIENT_ID')
    self.client_secret = flask_app.config.get('OPENID_CLIENT_SECRET')
    self.client_scopes = flask_app.config.get('OPENID_CLIENT_SCOPES')
    self.roles_attribute = flask_app.config.get('OPENID_ROLES_ATTRIBUTE').split('.')
    self.allowed_role = flask_app.config.get('OPENID_ALLOWED_ROLE')

    self._fetch_metadata()

    flask_app.openid = self

  def _fetch_metadata(self):
    try:
      response = requests.get(
        urljoin(self.discover_url, ".well-known/openid-configuration"),
        timeout=5
      )
      self.metadata = response.json()
    except Exception as error:
      self.logger.error("Unable to retreiv OpenID configuration")
      self.logger.error(error)

  def get_authn_url(self, state):
    query = urlencode(dict(
      client_id=self.client_id,
      redirect_uri=custom_url_for("openid.callback"),
      state=state,
      response_type="code",
      scope=self.client_scopes
    ))

    return f"{self.metadata.get('authorization_endpoint')}?{query}"

  def get_token(self, code):
    try:
      response = requests.post(
        self.metadata.get('token_endpoint'),
        timeout=5,
        data=dict(
          code=code,
          client_id=self.client_id,
          client_secret=self.client_secret,
          grant_type="authorization_code",
          redirect_uri=custom_url_for("openid.callback")
        )
      )
      return response.json()
    except Exception as error:
      self.logger.error("Unable to retreiv OpenID token")
      self.logger.error(error)

  def decode_token(self, token):
    return jwt.decode(
      jwt=token,
      options=dict(
        verify_signature=False
      )
    )

  def is_token_allowed(self, token_id):
    data = token_id
    for attr in self.roles_attribute:
      if attr not in data:
        return False

      data = data.get(attr)

    if isinstance(data, str):
      data = data.split("##")

    return self.allowed_role in data
