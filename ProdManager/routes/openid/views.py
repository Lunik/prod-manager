import os
import hashlib

from datetime import datetime

from flask import (
  Blueprint, redirect, abort, current_app,
  session, request
)

from ProdManager.plugins import oidc, lang
from ProdManager.helpers.auth import logout_required
from ProdManager.helpers.links import custom_url_for

bp = Blueprint("openid", __name__)

###########
## LOGIN ##
###########

@bp.route("/login", methods=("GET",))
@logout_required
def login():
  state = hashlib.sha256(os.urandom(1024)).hexdigest()
  session['state'] = state

  return redirect(oidc.get_authn_url(state=state), 302)


@bp.route("/callback", methods=("GET",))
@logout_required
def callback():
  if request.args.get('state') != session.get('state'):
    abort(401, dict(
      message=lang.get("openid_callback_failed"),
      reasons=dict(state=[lang.get("openid_invalid_state")])
    ))

  error = request.args.get('error_description')
  if error:
    abort(400, dict(
      message=lang.get("openid_callback_failed"),
      reasons=dict(callback=[error])
    ))

  code = request.args.get('code')
  if code is None:
    abort(401, dict(
      message=lang.get("openid_callback_failed"),
      reasons=dict(state=[lang.get("openid_invalid_code")])
    ))

  token = oidc.get_token(code=code)
  print(token)
  if token is None:
    abort(500, dict(
      message=lang.get("openid_callback_failed"),
      reasons=dict(token=[lang.get("openid_auth_failed")])
    ))

  error = token.get('error_description')
  if error :
    abort(401, dict(
      message=lang.get("openid_callback_failed"),
      reasons=dict(callback=[error])
    ))

  token_id = oidc.decode_token(token.get('id_token'))
  if not oidc.is_token_allowed(token_id):
    abort(403, dict(
      message=lang.get("openid_callback_failed"),
      reasons=dict(state=[lang.get("openid_not_enough_permissions")])
    ))

  current_app.logger.info(
    "Login succeed with OpenID for user : %s",
    token_id.get('preferred_username', 'undefined')
  )

  session.clear()
  session["logged"] = True
  session["logged_at"] = datetime.now().timestamp()

  return redirect(custom_url_for('root.index'), 302)
