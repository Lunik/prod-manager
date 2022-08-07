from datetime import datetime, timedelta

from flask import Blueprint, redirect, abort
from flask import current_app
from flask import g
from flask import session

from ProdManager import lang
from ProdManager.helpers.template import custom_render_template
from ProdManager.helpers.auth import logout_required
from ProdManager.helpers.links import custom_url_for

from .forms import AuthLoginForm

bp = Blueprint("auth", __name__)

###########
## LOGIN ##
###########

@bp.route("/login", methods=("GET",))
@logout_required
def login():
  form = AuthLoginForm()

  return custom_render_template("auth/login.html",
    form=form
  ), 200


@bp.route("/login", methods=("POST",))
@logout_required
def do_login():
  form = AuthLoginForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("auth_login_failed"),
      reasons=form.errors,
    ))

  if form.secret.data != current_app.config['SECRET_KEY']:
    abort(400, dict(
      message=lang.get("auth_login_failed"),
      reasons=dict(secret=[lang.get("auth_invalid_secret")]),
    ))

  remember_me_days = 1
  if form.remember_me.data:
    remember_me_days = 7

  session.clear()
  session["logged"] = True
  session["logged_at"] = datetime.now().timestamp()
  session["logged_until"] = (datetime.now() + timedelta(days=remember_me_days)).timestamp()

  return redirect(custom_url_for('root.index'), 302)

############
## LOGOUT ##
############

@bp.route("/logout", methods=("GET", "POST",))
def logout():
  session.clear()
  return redirect(custom_url_for('root.index'), 302)

############
## WHOAMI ##
############

@bp.route("/logged", methods=("GET",))
def whoami():
  return str(g.logged is not None and g.logged)
