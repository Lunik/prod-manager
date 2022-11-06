import functools
import uuid
import re
from datetime import datetime
import jwt

from flask import session, request, redirect, g, abort, current_app

from ProdManager.helpers.links import custom_url_for

from ProdManager.plugins import lang

JWT_REGEX = re.compile(r'(\w+)\s+([a-zA-Z0-9_=]+\.[a-zA-Z0-9_=]+\.[a-zA-Z0-9_\-\+\/=]+)')

def retreiv_auth():
  g.logged = False

  # API Authentication
  g.jwt = None
  try:
    api_token = get_api_token()
    if api_token:
      jwt_token = verify_jwt(api_token)
      g.jwt = jwt_token
  except Exception as error:
    abort(401, dict(
      message=lang.get("token_validation_failed"),
      reasons=dict(token=[str(error)])
    ))

  g.logged = (session.get("logged", None)) or (g.api and g.jwt)


def verify_token_permissions(jwt_token):
  if request.blueprint is None:
    return

  if request.blueprint not in jwt_token['permissions']:
    abort(403, dict(
      message=lang.get("api_permission_denied"),
      reasons=dict(
        token=[lang.get("token_not_enought_permissions") + request.blueprint]
      )
    ))


def login_required(view):
  """View decorator that redirects anonymous users to the login page."""

  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.logged:
      if g.api and g.jwt:
        verify_token_permissions(g.jwt)

      return view(**kwargs)

    return abort(403)

  return wrapped_view


def logout_required(view):
  """View decorator that redirects anonymous users to the login page."""

  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.logged:
      return redirect(custom_url_for('root.index'))

    return view(**kwargs)

  return wrapped_view

def get_api_token():
  value = request.headers.get('Authorization', None)
  if value is None:
    return None

  match = JWT_REGEX.match(value)
  if match is None:
    raise Exception(lang.get("token_invalid_format") + JWT_REGEX.pattern)

  return match.group(2)

JWT_TOKEN_VERSION=1

def generate_jwt(name, description, not_before_date, expiration_date, permissions):
  return jwt.encode(
    payload=dict(
      iss=current_app.config['JWT_ISSUER'],
      aud=name,
      sub=description,
      nbf=not_before_date,
      exp=expiration_date,
      iat=datetime.utcnow(),
      jti=str(uuid.uuid4()),
      version=JWT_TOKEN_VERSION,
      permissions=permissions,
    ),
    key=current_app.config['SECRET_KEY'],
    algorithm=current_app.config['JWT_ALGORITHM']
  )

def verify_jwt(token):
  jwt_token = jwt.decode(
    jwt=token,
    key=current_app.config['SECRET_KEY'],
    algorithms=[current_app.config['JWT_ALGORITHM']],
    options=dict(
      verify_signature=True,
      require=['iss', 'exp', 'nbf'],
      verify_aud=False
    ),
    issuer=current_app.config['JWT_ISSUER'],
  )

  if 'version' not in jwt_token or jwt_token['version'] != JWT_TOKEN_VERSION:
    raise Exception(lang.get("token_expired_version") + JWT_TOKEN_VERSION)

  return jwt_token
