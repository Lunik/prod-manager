
from flask import Blueprint, url_for, redirect, abort

from ProdManager import lang

from ProdManager.helpers.template import custom_render_template
from ProdManager.helpers.auth import login_required
from ProdManager.helpers.resource import (
  create_resource,
  list_resources,
  get_resource,
  update_resource,
  delete_resource,
  list_resources_as_choices,
  resource_filters,
)
from ProdManager.helpers.date import current_date
from ProdManager.helpers.form import strip_input

from ProdManager.models import (
  Incident, IncidentSeverity, IncidentStatus, Scope,
  Service, EventType, IncidentEvent,
)

from .forms import IncidentCreateForm, IncidentUpdateForm, IncidentCommentForm, IncidentDeleteForm

bp = Blueprint("incident", __name__)

##########
## LIST ##
##########

@bp.route("", methods=("GET",))
@resource_filters(Incident.filters())
def list(filters):
  incidents = list_resources(Incident, filters=filters)

  create_form = IncidentCreateForm()
  create_form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  create_form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  return custom_render_template("incident/list.html",
    incidents=incidents,
    create_form=create_form
  ), 200

############
## CREATE ##
############

@bp.route("/create", methods=("POST",))
@login_required
def create():
  form=IncidentCreateForm()
  form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("incident_creation_failed"),
      reasons=form.errors
    ))

  try:
    incident = create_resource(Incident, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
      severity=IncidentSeverity(form.severity.data),
      external_reference=strip_input(form.external_reference.data),
      scope_id=int(form.scope.data),
      service_id=int(form.service.data),
      creation_date=current_date(),
      start_impact_date=form.start_impact_date.data,
    ))
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("incident_creation_failed"),
      reasons=dict(incident=[error.message])
    ))

  return redirect(url_for('incident.show', resource_id=incident.id), 302)

##########
## SHOW ##
##########

@bp.route("/<int:resource_id>", methods=("GET",))
def show(resource_id):
  try:
    incident = get_resource(Incident, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("incident_show_failed"),
      reasons=dict(incident=[error.message])
    ))

  update_form = IncidentUpdateForm(obj=incident)
  update_form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  update_form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  update_form.scope.default = incident.scope.id
  update_form.service.default = incident.service.id
  update_form.scope.process(formdata=None)
  update_form.service.process(formdata=None)

  return custom_render_template("incident/single.html",
    incident=incident,
    update_form=update_form,
    comment_form=IncidentCommentForm(),
    delete_form=IncidentDeleteForm(obj=incident),
  ), 200


############
## UPDATE ##
############

@bp.route("/<int:resource_id>/update", methods=("POST",))
@login_required
def update(resource_id):
  form = IncidentUpdateForm()
  form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("incident_update_failed"),
      reasons=form.errors
    ))

  new_incident_status = IncidentStatus(form.status.data)
  new_data = dict(
    name=strip_input(form.name.data),
    description=strip_input(form.description.data),
    severity=IncidentSeverity(form.severity.data),
    status=new_incident_status,
    external_reference=strip_input(form.external_reference.data),
    scope_id=int(form.scope.data),
    service_id=int(form.service.data),
    start_impact_date=form.start_impact_date.data,
    investigation_date=form.investigation_date.data,
    stable_date=form.stable_date.data,
    resolve_date=form.resolve_date.data,
  )

  if new_incident_status == IncidentStatus.INVESTIGATING and new_data['investigation_date'] is None:
    new_data["investigation_date"] = current_date()
  elif new_incident_status < IncidentStatus.INVESTIGATING:
    new_data["investigation_date"] = None

  if new_incident_status == IncidentStatus.STABLE and new_data['stable_date'] is None:
    new_data["stable_date"] = current_date()
  elif new_incident_status < IncidentStatus.STABLE:
    new_data["stable_date"] = None

  if new_incident_status == IncidentStatus.RESOLVED and new_data['resolve_date'] is None:
    new_data["resolve_date"] = current_date()
  elif new_incident_status < IncidentStatus.RESOLVED:
    new_data["resolve_date"] = None

  try:
    incident, changed = update_resource(Incident, resource_id, new_data)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("incident_update_failed"),
      reasons=dict(incident=[error.message])
    ))

  return redirect(url_for('incident.show', resource_id=incident.id), 302)

#############
## COMMENT ##
#############

@bp.route("/<int:resource_id>/comment", methods=("POST",))
@login_required
def comment(resource_id):
  form = IncidentCommentForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("incident_comment_failed"),
      reasons=form.errors
    ))

  try:
    _ = create_resource(IncidentEvent, dict(
      creation_date=current_date(rounded=False),
      type=EventType.COMMENT,
      content=form.comment.data,
      internal=form.internal.data,
      incident_id=resource_id,
    ))
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("incident_comment_failed"),
      reasons=dict(incident=error.message)
    ))

  return redirect(url_for('incident.show', resource_id=resource_id), 302)

############
## DELETE ##
############

@bp.route("/<int:resource_id>/delete", methods=("POST",))
@login_required
def delete(resource_id):
  form = IncidentDeleteForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("incident_deletion_failed"),
      reasons=form.errors
    ))

  try:
    delete_resource(Incident, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("incident_deletion_failed"),
      reasons=dict(incident=error.message)
    ))

  return redirect(url_for('incident.list'), 302)
