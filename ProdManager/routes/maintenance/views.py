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

from ProdManager.models.Maintenance import Maintenance, MaintenanceStatus
from ProdManager.models.Scope import Scope
from ProdManager.models.Service import Service, ServiceStatus

from .forms import MaintenanceCreateForm, MaintenanceUpdateForm, MaintenanceDeleteForm

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
      scope_id=form.scope_id.data,
      service_id=form.service_id.data,
      creation_date=datetime.now(),
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
    scope_id=form.scope_id.data,
    service_id=form.service_id.data,
  )

  if new_maintenance_status == MaintenanceStatus.IN_PROGRESS:
    new_data["start_date"] = datetime.now()
  elif new_maintenance_status < MaintenanceStatus.IN_PROGRESS:
    new_data["start_date"] = None

  if new_maintenance_status in [MaintenanceStatus.SUCCEED, MaintenanceStatus.FAILED]:
    new_data["end_date"] = datetime.now()
  elif new_maintenance_status < MaintenanceStatus.SUCCEED:
    new_data["end_date"] = None

  try:
    maintenance, _ = update_resource(Maintenance, resource_id, new_data)
  except Exception as error:
    return abort(error.code, dict(
      message="Maintenance update failed",
      reasons=dict(maintenance=error.message)
    ))

  return redirect(url_for('maintenance.show', resource_id=maintenance.id), 302)

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
