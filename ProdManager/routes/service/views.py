
from flask import Blueprint, url_for, render_template, redirect, abort

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

from ProdManager.models import (
  Service, Monitor, Incident, Maintenance,
)

from .forms import ServiceCreateForm, ServiceUpdateForm, ServiceDeleteForm

bp = Blueprint("service", __name__)

##########
## LIST ##
##########

@bp.route("", methods=("GET",))
def list():
  services = list_resources(Service)

  return render_template("service/list.html",
    services=services,
    create_form=ServiceCreateForm()
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
      message="Service creation failed",
      reasons=form.errors
    ))

  try:
    service = create_resource(Service, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Service creation failed",
      reasons=dict(service=[error.message])
    ))

  return redirect(url_for('service.show', resource_id=service.id), 302)

##########
## SHOW ##
##########

@bp.route("/<int:resource_id>", methods=("GET",))
def show(resource_id):
  try:
    service = get_resource(Service, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message="Service show failed",
      reasons=dict(service=[error.message])
    ))

  update_form = ServiceUpdateForm(obj=service)

  return render_template("service/single.html",
    service=service,
    update_form=update_form,
    delete_form=ServiceDeleteForm(obj=service),
    ongoing_incidents=list_resources_from_query(
      Incident,
      query=service.incidents,
      filters=Incident.ongoing_filter(),
      orders=Incident.reverse_order(),
      paginate=False,
    ),
    past_incidents=list_resources_from_query(
      Incident,
      query=service.incidents,
      filters=Incident.past_filter(),
      paginate=False,
    ),
    scheduled_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.scheduled_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
    ),
    ongoing_maintenances=list_resources_from_query(
      Maintenance,
      query=service.maintenances,
      filters=Maintenance.ongoing_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
    ),
    past_maintenances=list_resources_from_query(
      Maintenance,
      query=service.maintenances,
      filters=Maintenance.past_filter(),
      paginate=False,
    ),
    monitors_count=Monitor.count_monitors(service.monitors),
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
      message="Service update failed",
      reasons=form.errors
    ))

  try:
    service, _ = update_resource(Service, resource_id, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Service update failed",
      reasons=dict(service=[error.message])
    ))

  return redirect(url_for('service.show', resource_id=service.id), 302)

############
## DELETE ##
############

@bp.route("/<int:resource_id>/delete", methods=("POST",))
@login_required
def delete(resource_id):
  form = ServiceDeleteForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message="Service deletion failed",
      reasons=form.errors
    ))

  try:
    delete_resource(Service, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message="Service deletion failed",
      reasons=dict(service=[error.message])
    ))

  return redirect(url_for('service.list'), 302)
