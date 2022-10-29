from flask import Blueprint, abort, current_app, g

from ProdManager.helpers.template import custom_render_template
from ProdManager.helpers.auth import login_required, generate_jwt
from ProdManager.helpers.form import strip_input

from ProdManager.plugins import lang

from .forms import TokenCreateForm

bp = Blueprint("token", __name__)

############
## CREATE ##
############

@bp.route("/create", methods=("POST",))
def create():
  form=TokenCreateForm()
  form.permission.choices = list(filter(lambda bp: '_api' in bp, current_app.blueprints.keys()))

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("token_creation_failed"),
      reasons=form.errors
    ))

  if form.secret.data != current_app.config['SECRET_KEY']:
    abort(400, dict(
      message=lang.get("token_creation_failed"),
      reasons=dict(secret=[lang.get("application_secret_invalid")])
    ))

  try:
    jwt = generate_jwt(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
      not_before_date=form.not_before_date.data,
      expiration_date=form.expiration_date.data,
      permissions=form.permission.data,
    )
  except Exception as error:
    return abort(500, dict(
      message=lang.get("token_creation_failed"),
      reasons=dict(token=[error])
    ))

  return custom_render_template(None,
    json=dict(resources=jwt, serialize=False),
  )

############
## WHOAMI ##
############

@bp.route("/whoami", methods=("GET",))
def whoami():
  return custom_render_template(None,
    json=dict(resources=dict(playload=g.jwt), serialize=False),
  )
