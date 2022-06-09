from datetime import datetime, timedelta

from flask import Blueprint,url_for, render_template, redirect
from flask import current_app
from flask import g
from flask import request
from flask import session

from ProdManager.helpers.auth import logout_required
from .forms import AuthLoginForm

bp = Blueprint("auth", __name__)

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

def show_login(_):
  return None, None, 200

def do_login(form):
  if not form.validate_on_submit():
    return None, dict(
      message="Login failed",
      reasons=form.errors
    ), 400

  if form.secret.data != current_app.config['SECRET_KEY']:
    return None, dict(
      message="Login failed",
      reasons=dict(secret="Invalid secret")
    ), 400

  session.clear()
  session["logged"] = True
  session["logged_at"] = datetime.now()
  session["logged_until"] = datetime.now() + timedelta(days=1)

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
  return str(g.logged is not None)
