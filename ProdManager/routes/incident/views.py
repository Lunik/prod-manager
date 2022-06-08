from datetime import datetime
from flask import Blueprint,url_for, render_template, redirect, abort

from ProdManager.helpers.auth import login_required
from ProdManager.helpers.resource import (
  create_resource,
  list_resources,
  get_resource,
  update_resource,
  delete_resource,
  list_resources_as_choices
)

from ProdManager.models.Incident import Incident, IncidentSeverity, IncidentStatus
from ProdManager.models.Scope import Scope
from ProdManager.models.Service import Service

from .forms import IncidentCreateForm, IncidentUpdateForm, IncidentDeleteForm

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
      scope_id=form.scope_id.data,
      service_id=form.service_id.data,
      creation_date=datetime.now(),
      start_impact_date=datetime.now(),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Incident creation failed",
      reasons=dict(incident=error.message)
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
      message="Incident show failed",
      reasons=dict(incident=error.message)
    ))

  update_form = IncidentUpdateForm(obj=incident)
  update_form.scope_id.choices = list_resources_as_choices(Scope)
  update_form.service_id.choices = list_resources_as_choices(Service)

  return render_template("incident/single.html",
    incident=incident,
    update_form=update_form,
    delete_form=IncidentDeleteForm(obj=incident)
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
    scope_id=form.scope_id.data,
    service_id=form.service_id.data,
    start_impact_date=form.start_impact_date.data,
  )

  if new_incident_status == IncidentStatus.INVESTIGATING:
    new_data["investigation_date"] = datetime.now()
  elif new_incident_status < IncidentStatus.INVESTIGATING:
    new_data["investigation_date"] = None

  if new_incident_status == IncidentStatus.STABLE:
    new_data["stable_date"] = datetime.now()
  elif new_incident_status < IncidentStatus.STABLE:
    new_data["stable_date"] = None

  if new_incident_status == IncidentStatus.RESOLVED:
    new_data["resolve_date"] = datetime.now()
  elif new_incident_status < IncidentStatus.RESOLVED:
    new_data["resolve_date"] = None

  try:
    incident, _ = update_resource(Incident, resource_id, new_data)
  except Exception as error:
    return abort(error.code, dict(
      message="Incident update failed",
      reasons=dict(incident=error.message)
    ))

  return redirect(url_for('incident.show', resource_id=incident.id), 302)

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
