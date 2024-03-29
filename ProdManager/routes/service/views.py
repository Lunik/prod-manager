
from flask import Blueprint, redirect, abort

from ProdManager.helpers.template import custom_render_template
from ProdManager.helpers.auth import login_required
from ProdManager.helpers.resource import (
  create_resource,
  list_resources,
  get_resource,
  update_resource,
  delete_resource,
  list_resources_from_query,
)
from ProdManager.helpers.form import strip_input
from ProdManager.helpers.links import custom_url_for

from ProdManager.models import (
  Service, Monitor, Incident, Maintenance, Announcement
)

from ProdManager.plugins import lang

from .forms import ServiceCreateForm, ServiceUpdateForm, ServiceDeleteForm

bp = Blueprint("service", __name__)

##########
## LIST ##
##########

@bp.route("", methods=("GET",))
def list():
  services = list_resources(Service)

  return custom_render_template("service/list.html",
    services=services,
    json=dict(resources=services),
    create_form=ServiceCreateForm(),
  ), 200


############
## CREATE ##
############

@bp.route("/create", methods=("POST",))
@login_required
def create():
  form=ServiceCreateForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("service_creation_failed"),
      reasons=form.errors
    ))

  try:
    service = create_resource(Service, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("service_creation_failed"),
      reasons=dict(service=[error.message])
    ))

  return redirect(custom_url_for('service.show', resource_id=service.id), 302)

##########
## SHOW ##
##########

@bp.route("/<int:resource_id>", methods=("GET",))
def show(resource_id):
  try:
    service = get_resource(Service, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("service_show_failed"),
      reasons=dict(service=[error.message])
    ))

  update_form = ServiceUpdateForm(obj=service)

  return custom_render_template("service/single.html",
    service=service,
    json=dict(resources=service),
    update_form=update_form,
    delete_form=ServiceDeleteForm(obj=service),
    ongoing_incidents_filters=Incident.ongoing_filter(raw=True),
    ongoing_incidents=list_resources_from_query(
      Incident,
      query=service.incidents,
      filters=Incident.ongoing_filter(),
      orders=Incident.reverse_order(),
      paginate=False,
      limit=10,
    ),
    past_incidents_filters=Incident.past_filter(raw=True),
    scheduled_maintenances_filters=Maintenance.scheduled_filter(raw=True),
    scheduled_maintenances=list_resources_from_query(
      Maintenance,
      query=service.maintenances,
      filters=Maintenance.scheduled_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
      limit=10,
    ),
    ongoing_maintenances_filters=Maintenance.ongoing_filter(raw=True),
    ongoing_maintenances=list_resources_from_query(
      Maintenance,
      query=service.maintenances,
      filters=Maintenance.ongoing_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
      limit=10,
    ),
    past_maintenances_filters=Maintenance.past_filter(raw=True),
    monitors_count=service.monitors_count(),
    ongoing_announcements_filters=Announcement.ongoing_filter(raw=True),
    ongoing_announcements=list_resources_from_query(
      Announcement,
      query=service.announcements,
      filters=Announcement.ongoing_filter(),
      orders=Announcement.reverse_order(),
      paginate=False,
      limit=10,
    ),
  ), 200


############
## UPDATE ##
############

@bp.route("/<int:resource_id>/update", methods=("POST",))
@login_required
def update(resource_id):
  form = ServiceUpdateForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("service_update_failed"),
      reasons=form.errors
    ))

  try:
    service, _ = update_resource(Service, resource_id, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("service_update_failed"),
      reasons=dict(service=[error.message])
    ))

  return redirect(custom_url_for('service.show', resource_id=service.id), 302)

############
## DELETE ##
############

@bp.route("/<int:resource_id>/delete", methods=("POST",))
@login_required
def delete(resource_id):
  form = ServiceDeleteForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("service_deletion_failed"),
      reasons=form.errors
    ))

  try:
    delete_resource(Service, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("service_deletion_failed"),
      reasons=dict(service=[error.message])
    ))

  return redirect(custom_url_for('service.list'), 302)
