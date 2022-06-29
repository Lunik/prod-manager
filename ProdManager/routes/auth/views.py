from datetime import datetime, timedelta

from flask import Blueprint,url_for, render_template, redirect, abort
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

@bp.route("/login", methods=("GET",))
@logout_required
def login():
  form = AuthLoginForm()

  return render_template("auth/login.html",
    form=form
  ), 200


@bp.route("/login", methods=("POST",))
@logout_required
def do_login():
  form = AuthLoginForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message="Login failed",
      reasons=form.errors,
    ))

  if form.secret.data != current_app.config['SECRET_KEY']:
    abort(400, dict(
      message="Login failed",
      reasons=dict(secret=["Invalid secret"]),
    ))

  session.clear()
  session["logged"] = True
  session["logged_at"] = datetime.now().timestamp()
  session["logged_until"] = (datetime.now() + timedelta(days=1)).timestamp()

  return redirect(url_for('root.index'), 302)

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
