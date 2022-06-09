from datetime import datetime
import functools

from flask import session, redirect, url_for, g, abort

def retreiv_auth():
  logged_until = session.get("logged_until", None)

  #raise Exception(logged_until)

  if logged_until and (datetime.now() > datetime.fromtimestamp(logged_until)):
    session.clear()

  g.logged = session.get("logged", None)


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
      return redirect(url_for('root.index'))

    return view(**kwargs)

  return wrapped_view
