from flask import Blueprint,url_for, render_template, redirect, abort

from ProdManager.helpers.auth import login_required
from ProdManager.helpers.resource import create_resource, list_resources, get_resource, update_resource, delete_resource
from ProdManager.models.Scope import Scope
from ProdManager.models.Incident import filter_ongoing_incident, filter_past_incident
from ProdManager.models.Maintenance import filter_ongoing_maintenance, filter_past_maintenance

from .forms import ScopeCreateForm, ScopeUpdateForm, ScopeDeleteForm

bp = Blueprint("scope", __name__)

##########
## LIST ##
##########

@bp.route("", methods=("GET",))
def list():
  scopes = list_resources(Scope)

  return render_template("scope/list.html",
    scopes=scopes,
    create_form=ScopeCreateForm()
  ), 200

############
## CREATE ##
############

@bp.route("/create", methods=("POST",))
@login_required
def create():
  form=ScopeCreateForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message="Scope creation failed",
      reasons=form.errors
    ))

  try:
    scope = create_resource(Scope, dict(
      name=form.name.data,
      description=form.description.data,
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Scope creation failed",
      reasons=dict(scope=error.message)
    ))

  return redirect(url_for('scope.show', resource_id=scope.id), 302)

##########
## SHOW ##
##########

@bp.route("/<int:resource_id>", methods=("GET",))
def show(resource_id):
  try:
    scope = get_resource(Scope, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message="Scope show failed",
      reasons=dict(scope=error.message)
    ))

  return render_template("scope/single.html",
    scope=scope,
    update_form=ScopeUpdateForm(obj=scope),
    delete_form=ScopeDeleteForm(obj=scope),
    ongoing_incidents=filter_ongoing_incident(scope.incidents),
    past_incidents=filter_past_incident(scope.incidents),
    ongoing_maintenances=filter_ongoing_maintenance(scope.maintenances),
    past_maintenances=filter_past_maintenance(scope.maintenances),
  ), 200


############
## UPDATE ##
############

@bp.route("/<int:resource_id>/update", methods=("POST",))
@login_required
def update(resource_id):
  form = ScopeUpdateForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message="Scope update failed",
      reasons=form.errors
    ))

  try:
    scope, _ = update_resource(Scope, resource_id, dict(
      name=form.name.data,
      description=form.description.data,
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Scope update failed",
      reasons=dict(scope=error.message)
    ))

  return redirect(url_for('scope.show', resource_id=scope.id), 302)

############
## DELETE ##
############

@bp.route("/<int:resource_id>/delete", methods=("POST",))
@login_required
def delete(resource_id):
  form = ScopeDeleteForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message="Scope deletion failed",
      reasons=form.errors
    ))

  try:
    delete_resource(Scope, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message="Scope deletion failed",
      reasons=dict(scope=error.message)
    ))

  return redirect(url_for('scope.list'), 302)
