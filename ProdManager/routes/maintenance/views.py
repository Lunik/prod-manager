import json
from flask import Blueprint,url_for, render_template, redirect, abort, current_app

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

from ProdManager.models.Maintenance import Maintenance, MaintenanceStatus
from ProdManager.models.Scope import Scope
from ProdManager.models.Service import Service, ServiceStatus
from ProdManager.models.Event import EventType
from ProdManager.models.MaintenanceEvent import MaintenanceEvent

from .forms import MaintenanceCreateForm, MaintenanceUpdateForm, MaintenanceCommentForm, MaintenanceDeleteForm

bp = Blueprint("maintenance", __name__)

##########
## LIST ##
##########

@bp.route("", methods=("GET",))
def list():
  maintenances = list_resources(Maintenance)

  create_form = MaintenanceCreateForm()
  create_form.scope_id.choices = list_resources_as_choices(Scope)
  create_form.service_id.choices = list_resources_as_choices(Service)

  return render_template("maintenance/list.html",
    maintenances=maintenances,
    create_form=create_form
  ), 200

############
## CREATE ##
############

@bp.route("/create", methods=("POST",))
@login_required
def create():
  form=MaintenanceCreateForm()
  form.scope_id.choices = list_resources_as_choices(Scope)
  form.service_id.choices = list_resources_as_choices(Service)

  if not form.validate_on_submit():
    abort(400, dict(
      message="Maintenance creation failed",
      reasons=form.errors
    ))

  try:
    maintenance = create_resource(Maintenance, dict(
      name=form.name.data,
      description=form.description.data,
      external_reference=form.external_reference.data,
      scope_id=int(form.scope_id.data),
      service_id=int(form.service_id.data),
      creation_date=current_date(),
      scheduled_start_date=form.scheduled_start_date.data,
      scheduled_end_date=form.scheduled_end_date.data,
      service_status=ServiceStatus(form.service_status.data),
      status=MaintenanceStatus.SCHEDULED
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Maintenance creation failed",
      reasons=dict(maintenance=error.message)
    ))

  try:
    event = create_resource(MaintenanceEvent, dict(
      creation_date=current_date(rounded=False),
      type=EventType.CREATE,
      content=json.dumps(maintenance.serialize, default=json_defaults),
      maintenance_id=maintenance.id,
    ))
  except Exception as error:
    current_app.logger.error(f"Unable to create event during Maintenance creation : {error}")

  return redirect(url_for('maintenance.show', resource_id=maintenance.id), 302)

##########
## SHOW ##
##########

@bp.route("/<int:resource_id>", methods=("GET",))
def show(resource_id):
  try:
    maintenance = get_resource(Maintenance, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message="Maintenance show failed",
      reasons=dict(maintenance=error.message)
    ))

  update_form = MaintenanceUpdateForm(obj=maintenance)
  update_form.scope_id.choices = list_resources_as_choices(Scope)
  update_form.service_id.choices = list_resources_as_choices(Service)

  return render_template("maintenance/single.html",
    maintenance=maintenance,
    update_form=update_form,
    comment_form=MaintenanceCommentForm(),
    delete_form=MaintenanceDeleteForm(obj=maintenance)
  ), 200


############
## UPDATE ##
############

@bp.route("/<int:resource_id>/update", methods=("POST",))
@login_required
def update(resource_id):
  form = MaintenanceUpdateForm()
  form.scope_id.choices = list_resources_as_choices(Scope)
  form.service_id.choices = list_resources_as_choices(Service)

  if not form.validate_on_submit():
    abort(400, dict(
      message="Maintenance update failed",
      reasons=form.errors
    ))

  new_maintenance_status = MaintenanceStatus(form.status.data)
  new_data = dict(
    name=form.name.data,
    external_reference=form.external_reference.data,
    description=form.description.data,
    status=new_maintenance_status,
    scheduled_start_date=form.scheduled_start_date.data,
    scheduled_end_date=form.scheduled_end_date.data,
    service_status=ServiceStatus(form.service_status.data),
    scope_id=int(form.scope_id.data),
    service_id=int(form.service_id.data),
  )

  if new_maintenance_status == MaintenanceStatus.IN_PROGRESS:
    new_data["start_date"] = current_date()
  elif new_maintenance_status < MaintenanceStatus.IN_PROGRESS:
    new_data["start_date"] = None

  if new_maintenance_status in [MaintenanceStatus.SUCCEED, MaintenanceStatus.FAILED]:
    new_data["end_date"] = current_date()
  elif new_maintenance_status < MaintenanceStatus.SUCCEED:
    new_data["end_date"] = None

  try:
    maintenance, changed = update_resource(Maintenance, resource_id, new_data)
  except Exception as error:
    return abort(error.code, dict(
      message="Maintenance update failed",
      reasons=dict(maintenance=error.message)
    ))

  if len(changed) > 0:
    try:
      event = create_resource(MaintenanceEvent, dict(
        creation_date=current_date(rounded=False),
        type=EventType.UPDATE,
        content=json.dumps(changed, default=json_defaults),
        maintenance_id=maintenance.id,
      ))
    except Exception as error:
      current_app.logger.error(f"Unable to create event during Maintenance update : {error}")

  return redirect(url_for('maintenance.show', resource_id=maintenance.id), 302)

#############
## COMMENT ##
#############

@bp.route("/<int:resource_id>/comment", methods=("POST",))
@login_required
def comment(resource_id):
  form = MaintenanceCommentForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message="Maintenance comment failed",
      reasons=form.errors
    ))

  try:
    event = create_resource(MaintenanceEvent, dict(
      creation_date=current_date(rounded=False),
      type=EventType.COMMENT,
      content=form.comment.data,
      maintenance_id=resource_id,
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Maintenance update failed",
      reasons=dict(maintenance=error.message)
    ))

  return redirect(url_for('maintenance.show', resource_id=resource_id), 302)

############
## DELETE ##
############

@bp.route("/<int:resource_id>/delete", methods=("POST",))
@login_required
def delete(resource_id):
  form = MaintenanceDeleteForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message="Maintenance deletion failed",
      reasons=form.errors
    ))

  try:
    delete_resource(Maintenance, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message="Maintenance deletion failed",
      reasons=dict(maintenance=error.message)
    ))

  return redirect(url_for('maintenance.list'), 302)
