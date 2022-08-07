from flask import Blueprint, redirect, abort

from ProdManager.helpers.template import custom_render_template
from ProdManager.helpers.auth import login_required
from ProdManager.helpers.resource import (
  create_resource, list_resources, get_resource,
  update_resource, delete_resource, list_resources_from_query,
)
from ProdManager.helpers.form import strip_input
from ProdManager.helpers.links import custom_url_for

from ProdManager.models import (
  Scope, Monitor, Incident, Maintenance,
)

from ProdManager import lang

from .forms import ScopeCreateForm, ScopeUpdateForm, ScopeDeleteForm

bp = Blueprint("scope", __name__)

##########
## LIST ##
##########

@bp.route("", methods=("GET",))
def list():
  scopes = list_resources(Scope)

  return custom_render_template("scope/list.html",
    scopes=scopes,
    json=dict(resources=scopes),
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
      message=lang.get("scope_creation_failed"),
      reasons=form.errors
    ))

  try:
    scope = create_resource(Scope, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("scope_creation_failed"),
      reasons=dict(scope=[error.message])
    ))

  return redirect(custom_url_for('scope.show', resource_id=scope.id), 302)

##########
## SHOW ##
##########

@bp.route("/<int:resource_id>", methods=("GET",))
def show(resource_id):
  try:
    scope = get_resource(Scope, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("scope_show_failed"),
      reasons=dict(scope=[error.message])
    ))

  return custom_render_template("scope/single.html",
    scope=scope,
    json=dict(resources=scope),
    update_form=ScopeUpdateForm(obj=scope),
    delete_form=ScopeDeleteForm(obj=scope),
    ongoing_incidents=list_resources_from_query(
      Incident,
      query=scope.incidents,
      filters=Incident.ongoing_filter(),
      orders=Incident.reverse_order(),
      paginate=False,
      limit=10,
    ),
    past_incidents=list_resources_from_query(
      Incident,
      query=scope.incidents,
      filters=Incident.past_filter(),
      paginate=False,
      limit=10,
    ),
    scheduled_maintenances=list_resources_from_query(
      Maintenance,
      query=scope.maintenances,
      filters=Maintenance.scheduled_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
      limit=10,
    ),
    ongoing_maintenances=list_resources_from_query(
      Maintenance,
      query=scope.maintenances,
      filters=Maintenance.ongoing_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
      limit=10,
    ),
    past_maintenances=list_resources_from_query(
      Maintenance,
      query=scope.maintenances,
      filters=Maintenance.past_filter(),
      paginate=False,
      limit=10,
    ),
    monitors_count=Monitor.count_monitors(scope.monitors),
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
      message=lang.get("scope_update_failed"),
      reasons=form.errors
    ))

  try:
    scope, _ = update_resource(Scope, resource_id, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("scope_update_failed"),
      reasons=dict(scope=[error.message])
    ))

  return redirect(custom_url_for('scope.show', resource_id=scope.id), 302)

############
## DELETE ##
############

@bp.route("/<int:resource_id>/delete", methods=("POST",))
@login_required
def delete(resource_id):
  form = ScopeDeleteForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("scope_deletion_failed"),
      reasons=form.errors
    ))

  try:
    delete_resource(Scope, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("scope_deletion_failed"),
      reasons=dict(scope=[error.message])
    ))

  return redirect(custom_url_for('scope.list'), 302)
