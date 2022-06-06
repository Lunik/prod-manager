
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

from ProdManager.models.Service import Service
from ProdManager.models.Incident import filter_ongoing_incident, filter_past_incident
from ProdManager.models.Maintenance import filter_ongoing_maintenance, filter_past_maintenance

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
      name=form.name.data,
      description=form.description.data,
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Service creation failed",
      reasons=dict(service=error.message)
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
      reasons=dict(service=error.message)
    ))

  update_form = ServiceUpdateForm(obj=service)

  return render_template("service/single.html",
    service=service,
    update_form=update_form,
    delete_form=ServiceDeleteForm(obj=service),
    ongoing_incidents=filter_ongoing_incident(service.incidents),
    past_incidents=filter_past_incident(service.incidents),
    ongoing_maintenances=filter_ongoing_maintenance(service.maintenances),
    past_maintenances=filter_past_maintenance(service.maintenances),
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
      name=form.name.data,
      description=form.description.data,
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Service update failed",
      reasons=dict(service=error.message)
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
      reasons=dict(service=error.message)
    ))

  return redirect(url_for('service.list'), 302)
