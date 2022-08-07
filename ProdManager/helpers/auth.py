from datetime import datetime
import functools

from flask import session, request, redirect, g, abort, current_app

from ProdManager.helpers.links import custom_url_for

def retreiv_auth():
  logged_until = session.get("logged_until", None)

  if logged_until and (datetime.now() > datetime.fromtimestamp(logged_until)):
    session.clear()

  # API Authentication
  valid_header_token = (
    request.headers.get("APPLICATION-SECRET", None) == current_app.config['SECRET_KEY']
  )

  g.logged = (session.get("logged", None)) or valid_header_token


def login_required(view):
  """View decorator that redirects anonymous users to the login page."""

  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.logged:
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
