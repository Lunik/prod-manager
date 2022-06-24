from flask import Blueprint, url_for, render_template, redirect, abort

from ProdManager.helpers.auth import login_required
from ProdManager.helpers.resource import (
  create_resource, list_resources, get_resource,
  update_resource, delete_resource, list_resources_from_query,
)
from ProdManager.helpers.form import strip_input

from ProdManager.models.Scope import Scope
from ProdManager.models.Monitor import count_monitors
from ProdManager.models.Incident import Incident
from ProdManager.models.Maintenance import Maintenance

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
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
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
    ongoing_incidents=list_resources_from_query(
      Incident,
      query=scope.incidents,
      filters=Incident.ongoing_filter(),
      orders=Incident.reverse_order(),
      paginate=False,
    ),
    past_incidents=list_resources_from_query(
      Incident,
      query=scope.incidents,
      filters=Incident.past_filter(),
      paginate=False,
    ),
    ongoing_maintenances=list_resources_from_query(
      Maintenance,
      query=scope.maintenances,
      filters=Maintenance.ongoing_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
    ),
    past_maintenances=list_resources_from_query(
      Maintenance,
      query=scope.maintenances,
      filters=Maintenance.past_filter(),
      paginate=False,
    ),
    monitors_count=count_monitors(scope.monitors),
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
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
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
