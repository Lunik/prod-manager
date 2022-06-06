from datetime import datetime

from flask import Blueprint,url_for, render_template, redirect
from flask import current_app
from flask import g
from flask import request
from flask import session

from ProdManager.helpers.auth import logout_required, generate_jwt, verify_jwt
from .forms import AuthTokenForm, AuthLoginForm

bp = Blueprint("auth", __name__)

###########
## TOKEN ##
###########

@bp.route("/token", methods=("GET", "POST",))
def token():
  form = AuthTokenForm()

  token, error, code = dict(
    GET=show_generate_token,
    POST=do_generate_token
  )[request.method](form)

  return render_template("auth/token.html",
    token=token,
    error=error,
    form=form
  ), code

def show_generate_token(form):
  return None, None, 200

def do_generate_token(form):
  if not form.validate_on_submit():
    return None, dict(
      message="Token generation failed",
      reasons=form.errors
    ), 400

  if form.secret.data != current_app.config['SECRET_KEY']:
    return None, dict(
      message="Token generation failed",
      reasons=dict(secret="Invalid secret key")
    ), 400

  delta = form.expiration.data - datetime.now()

  duration = dict(
    days=delta.days,
    hours=0,
    minutes=0,
    seconds=delta.seconds
  )

  token = generate_jwt(
    metadata=dict(
      remote_addr=request.remote_addr
    ), **duration
  )

  return token, None, 200

###########
## LOGIN ##
###########

@bp.route("/login", methods=("GET", "POST",))
@logout_required
def login():
  form = AuthLoginForm()

  redirect_to, error, code = dict(
    GET=show_login,
    POST=do_login
  )[request.method](form)

  if redirect_to:
    return redirect(redirect_to, 302)


  return render_template("auth/login.html",
    error=error,
    form=form
  ), code

def show_login(form):
  return None, None, 200

def do_login(form):
  if not form.validate_on_submit():
    return None, dict(
      message="Login failed",
      reasons=form.errors
    ), 400

  jwt_is_valid, _, jwt_error = verify_jwt(form.token.data)
  if not jwt_is_valid:
    return None, dict(
      message="Login failed",
      reasons=dict(token=jwt_error)
    ), 400

  session.clear()
  session["jwt"] = form.token.data

  return url_for('root.index'), None, None

############
## LOGOUT ##
############

@bp.route("/logout", methods=("GET", "POST",))
def logout():
  session.clear()
  return redirect(url_for('root.index'), 302)

############
## WHOAMI ##
############

@bp.route("/logged", methods=("GET",))
def whoami():
  return str(g.jwt is not None)
