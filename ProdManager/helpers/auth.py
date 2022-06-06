from datetime import datetime, timedelta
import functools

import jwt
from flask import session, current_app, redirect, url_for, g, abort, request

def retreiv_auth():
  g.jwt = None

  jwt_token = request.headers.get('X-PRIVATE-TOKEN') or session.get("jwt")

  if jwt_token:
    is_valid, playload, _ = verify_jwt(jwt_token)
    if is_valid:
      g.jwt = playload


def login_required(view):
  """View decorator that redirects anonymous users to the login page."""

  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.jwt:
      return view(**kwargs)

    return abort(403)

  return wrapped_view


def logout_required(view):
  """View decorator that redirects anonymous users to the login page."""

  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.jwt:
      return redirect(url_for('root.index'))

    return view(**kwargs)

  return wrapped_view


def generate_jwt(days, hours, minutes, seconds, metadata=None):
  playload = dict(
    iss=current_app.config['APP_NAME'],
    iat=datetime.now(),
    exp=datetime.now() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds),
    metadata=metadata or dict(),
  )

  return jwt.encode(
    playload,
    current_app.config['SECRET_KEY'],
    algorithm=current_app.config['JWT_ALGORITHM'],
  )


def verify_jwt(encoded):
  is_valid = True
  playload = dict()
  error = None

  try:
    playload = jwt.decode(
      encoded,
      current_app.config['SECRET_KEY'],
      algorithms=current_app.config['JWT_ALGORITHM'],
    )
  except Exception as err:
    is_valid = False
    error = err

  return is_valid, playload, error
