from flask import Blueprint, redirect, abort, Response

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
from ProdManager.helpers.calendar import CalendarEvent
from ProdManager.helpers.links import custom_url_for

from ProdManager.models import (
  Maintenance, MaintenanceStatus, Scope, Service,
  ServiceStatus, EventType, MaintenanceEvent,
)

from .forms import (
  MaintenanceCreateForm, MaintenanceUpdateForm, MaintenanceCommentForm,
  MaintenanceDeleteForm,
)

bp = Blueprint("maintenance", __name__)

##########
## LIST ##
##########

@bp.route("", methods=("GET",))
@resource_filters(Maintenance.filters())
def list(filters):
  maintenances = list_resources(Maintenance, filters=filters)

  create_form = MaintenanceCreateForm()
  create_form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  create_form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  return custom_render_template("maintenance/list.html",
    maintenances=maintenances,
    json=dict(resources=maintenances),
    create_form=create_form,
    filters=Maintenance.filters().keys(),
  ), 200


############
## CREATE ##
############

@bp.route("/create", methods=("POST",))
@login_required
def create():
  form=MaintenanceCreateForm()
  form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("maintenance_creation_failed"),
      reasons=form.errors
    ))

  try:
    maintenance = create_resource(Maintenance, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
      external_reference=strip_input(form.external_reference.data),
      external_link=strip_input(form.external_link.data),
      scope_id=int(form.scope.data),
      service_id=int(form.service.data),
      creation_date=current_date(),
      scheduled_start_date=form.scheduled_start_date.data,
      scheduled_end_date=form.scheduled_end_date.data,
      service_status=ServiceStatus(form.service_status.data),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("maintenance_creation_failed"),
      reasons=dict(maintenance=[error.message])
    ))

  return redirect(custom_url_for('maintenance.show', resource_id=maintenance.id), 302)

##########
## SHOW ##
##########

@bp.route("/<int:resource_id>", methods=("GET",))
def show(resource_id):
  try:
    maintenance = get_resource(Maintenance, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("maintenance_show_failed"),
      reasons=dict(maintenance=[error.message])
    ))

  update_form = MaintenanceUpdateForm(obj=maintenance)
  update_form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  update_form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  update_form.scope.default = maintenance.scope.id
  update_form.service.default = maintenance.service.id
  update_form.scope.process(formdata=None)
  update_form.service.process(formdata=None)

  return custom_render_template("maintenance/single.html",
    maintenance=maintenance,
    json=dict(resources=maintenance),
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
  form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("maintenance_update_failed"),
      reasons=form.errors
    ))

  new_maintenance_status = MaintenanceStatus(form.status.data)
  new_data = dict(
    name=strip_input(form.name.data),
    external_reference=strip_input(form.external_reference.data),
    external_link=strip_input(form.external_link.data),
    description=strip_input(form.description.data),
    status=new_maintenance_status,
    scheduled_start_date=form.scheduled_start_date.data,
    scheduled_end_date=form.scheduled_end_date.data,
    start_date=form.start_date.data,
    end_date=form.end_date.data,
    service_status=ServiceStatus(form.service_status.data),
    scope_id=int(form.scope.data),
    service_id=int(form.service.data),
  )

  if new_maintenance_status == MaintenanceStatus.IN_PROGRESS and new_data['start_date'] is None:
    new_data["start_date"] = current_date()
  elif new_maintenance_status < MaintenanceStatus.IN_PROGRESS:
    new_data["start_date"] = None

  if new_maintenance_status in [MaintenanceStatus.SUCCEED, MaintenanceStatus.FAILED] and new_data['end_date'] is None:
    new_data["end_date"] = current_date()
  elif new_maintenance_status < MaintenanceStatus.SUCCEED:
    new_data["end_date"] = None

  try:
    maintenance, _ = update_resource(Maintenance, resource_id, new_data)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("maintenance_update_failed"),
      reasons=dict(maintenance=[error.message])
    ))

  return redirect(custom_url_for('maintenance.show', resource_id=maintenance.id), 302)

#############
## COMMENT ##
#############

@bp.route("/<int:resource_id>/comment", methods=("POST",))
@login_required
def comment(resource_id):
  form = MaintenanceCommentForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get('maintenance_comment_failed'),
      reasons=form.errors
    ))

  try:
    _ = create_resource(MaintenanceEvent, dict(
      creation_date=current_date(rounded=False),
      type=EventType.COMMENT,
      content=form.comment.data,
      internal=form.internal.data,
      maintenance_id=resource_id,
    ))
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get('maintenance_comment_failed'),
      reasons=dict(maintenance=[error.message])
    ))

  return redirect(custom_url_for('maintenance.show', resource_id=resource_id), 302)

############
## DELETE ##
############

@bp.route("/<int:resource_id>/delete", methods=("POST",))
@login_required
def delete(resource_id):
  form = MaintenanceDeleteForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get('maintenance_deletion_failed'),
      reasons=form.errors
    ))

  try:
    delete_resource(Maintenance, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get('maintenance_deletion_failed'),
      reasons=dict(maintenance=[error.message])
    ))

  return redirect(custom_url_for('maintenance.list'), 302)

##############
## CALENDAR ##
##############

@bp.route("/<int:resource_id>/calendar", methods=("GET",))
def calendar(resource_id):
  try:
    maintenance = get_resource(Maintenance, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("maintenance_show_failed"),
      reasons=dict(maintenance=[error.message])
    ))

  response = Response(
    response=CalendarEvent.from_maintenance(maintenance).render(),
    content_type="text/calendar",
  )
  response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{maintenance.name}.ics"
  return response, 200
