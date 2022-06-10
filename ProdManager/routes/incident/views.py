import json

from flask import Blueprint, url_for, render_template, redirect, abort, current_app

from ProdManager.helpers.auth import login_required
from ProdManager.helpers.resource import (
  create_resource,
  list_resources,
  get_resource,
  update_resource,
  delete_resource,
  list_resources_as_choices
)
from ProdManager.helpers.date import current_date
from ProdManager.helpers.json import json_defaults

from ProdManager.models.Incident import Incident, IncidentSeverity, IncidentStatus
from ProdManager.models.Scope import Scope
from ProdManager.models.Service import Service
from ProdManager.models.Event import EventType
from ProdManager.models.IncidentEvent import IncidentEvent

from .forms import IncidentCreateForm, IncidentUpdateForm, IncidentCommentForm, IncidentDeleteForm

bp = Blueprint("incident", __name__)

##########
## LIST ##
##########

@bp.route("", methods=("GET",))
def list():
  incidents = list_resources(Incident)

  create_form = IncidentCreateForm()
  create_form.scope_id.choices = list_resources_as_choices(Scope)
  create_form.service_id.choices = list_resources_as_choices(Service)

  return render_template("incident/list.html",
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
  form.scope_id.choices = list_resources_as_choices(Scope)
  form.service_id.choices = list_resources_as_choices(Service)

  if not form.validate_on_submit():
    abort(400, dict(
      message="Incident creation failed",
      reasons=form.errors
    ))

  try:
    incident = create_resource(Incident, dict(
      name=form.name.data,
      description=form.description.data,
      severity=IncidentSeverity(form.severity.data),
      external_reference=form.external_reference.data,
      scope_id=int(form.scope_id.data),
      service_id=int(form.service_id.data),
      creation_date=current_date(),
      start_impact_date=current_date(),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Incident creation failed",
      reasons=dict(incident=error.message)
    ))

  try:
    _ = create_resource(IncidentEvent, dict(
      creation_date=current_date(rounded=False),
      type=EventType.CREATE,
      content=json.dumps(incident.serialize, default=json_defaults),
      incident_id=incident.id,
    ))
  except Exception as error:
    current_app.logger.error(f"Unable to create event during Incident creation : {error}")

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
      message="Incident show failed",
      reasons=dict(incident=error.message)
    ))

  update_form = IncidentUpdateForm(obj=incident)
  update_form.scope_id.choices = list_resources_as_choices(Scope)
  update_form.service_id.choices = list_resources_as_choices(Service)

  return render_template("incident/single.html",
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
  form.scope_id.choices = list_resources_as_choices(Scope)
  form.service_id.choices = list_resources_as_choices(Service)

  if not form.validate_on_submit():
    abort(400, dict(
      message="Incident update failed",
      reasons=form.errors
    ))

  new_incident_status = IncidentStatus(form.status.data)
  new_data = dict(
    name=form.name.data,
    description=form.description.data,
    severity=IncidentSeverity(form.severity.data),
    status=new_incident_status,
    external_reference=form.external_reference.data,
    scope_id=int(form.scope_id.data),
    service_id=int(form.service_id.data),
    start_impact_date=form.start_impact_date.data,
  )

  if new_incident_status == IncidentStatus.INVESTIGATING:
    new_data["investigation_date"] = current_date()
  elif new_incident_status < IncidentStatus.INVESTIGATING:
    new_data["investigation_date"] = None

  if new_incident_status == IncidentStatus.STABLE:
    new_data["stable_date"] = current_date()
  elif new_incident_status < IncidentStatus.STABLE:
    new_data["stable_date"] = None

  if new_incident_status == IncidentStatus.RESOLVED:
    new_data["resolve_date"] = current_date()
  elif new_incident_status < IncidentStatus.RESOLVED:
    new_data["resolve_date"] = None

  try:
    incident, changed = update_resource(Incident, resource_id, new_data)
  except Exception as error:
    return abort(error.code, dict(
      message="Incident update failed",
      reasons=dict(incident=error.message)
    ))

  if len(changed) > 0:
    try:
      _ = create_resource(IncidentEvent, dict(
        creation_date=current_date(rounded=False),
        type=EventType.UPDATE,
        content=json.dumps(changed, default=json_defaults),
        incident_id=incident.id,
      ))
    except Exception as error:
      current_app.logger.error(f"Unable to create event during Incident update : {error}")

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
      message="Incident comment failed",
      reasons=form.errors
    ))

  try:
    _ = create_resource(IncidentEvent, dict(
      creation_date=current_date(rounded=False),
      type=EventType.COMMENT,
      content=form.comment.data,
      incident_id=resource_id,
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Incident update failed",
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
      message="Incident deletion failed",
      reasons=form.errors
    ))

  try:
    delete_resource(Incident, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message="Incident deletion failed",
      reasons=dict(incident=error.message)
    ))

  return redirect(url_for('incident.list'), 302)
