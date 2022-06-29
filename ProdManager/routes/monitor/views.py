from flask import Blueprint, url_for, render_template, redirect, abort

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
from ProdManager.helpers.form import strip_input

from ProdManager.models import (
  Monitor, MonitorStatus, Scope, Service,
)

from .forms import MonitorCreateForm, MonitorUpdateForm, MonitorDeleteForm

bp = Blueprint("monitor", __name__)

##########
## LIST ##
##########

@bp.route("", methods=("GET",))
@resource_filters(Monitor.filters())
def list(filters):

  monitors = list_resources(Monitor, filters=filters)

  create_form = MonitorCreateForm()
  create_form.scope_id.choices = list_resources_as_choices(Scope, Scope.name.asc())
  create_form.service_id.choices = list_resources_as_choices(Service, Service.name.asc())

  return render_template("monitor/list.html",
    monitors=monitors,
    create_form=create_form
  ), 200

############
## CREATE ##
############

@bp.route("/create", methods=("POST",))
@login_required
def create():
  form=MonitorCreateForm()
  form.scope_id.choices = list_resources_as_choices(Scope, Scope.name.asc())
  form.service_id.choices = list_resources_as_choices(Service, Service.name.asc())

  if not form.validate_on_submit():
    abort(400, dict(
      message="MonitorCreateForm creation failed",
      reasons=form.errors
    ))

  try:
    monitor = create_resource(Monitor, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
      external_link=strip_input(form.external_link.data),
      scope_id=int(form.scope_id.data),
      service_id=int(form.service_id.data),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="MonitorCreateForm creation failed",
      reasons=dict(monitor=[error.message])
    ))

  return redirect(url_for('monitor.show', resource_id=monitor.id), 302)

##########
## SHOW ##
##########

@bp.route("/<int:resource_id>", methods=("GET",))
def show(resource_id):
  try:
    monitor = get_resource(Monitor, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message="monitor show failed",
      reasons=dict(monitor=[error.message])
    ))

  update_form = MonitorUpdateForm(obj=monitor)
  update_form.scope_id.choices = list_resources_as_choices(Scope, Scope.name.asc())
  update_form.service_id.choices = list_resources_as_choices(Service, Service.name.asc())

  return render_template("monitor/single.html",
    monitor=monitor,
    update_form=update_form,
    delete_form=MonitorDeleteForm(obj=monitor),
  ), 200


############
## UPDATE ##
############

@bp.route("/<int:resource_id>/update", methods=("POST",))
@login_required
def update(resource_id):
  form = MonitorUpdateForm()
  form.scope_id.choices = list_resources_as_choices(Scope, Scope.name.asc())
  form.service_id.choices = list_resources_as_choices(Service, Service.name.asc())

  if not form.validate_on_submit():
    abort(400, dict(
      message="Monitor update failed",
      reasons=form.errors
    ))

  try:
    monitor, _ = update_resource(Monitor, resource_id, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
      external_link=strip_input(form.external_link.data),
      scope_id=int(form.scope_id.data),
      service_id=int(form.service_id.data),
      status=MonitorStatus(form.status.data),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message="Monitor update failed",
      reasons=dict(monitor=[error.message])
    ))

  return redirect(url_for('monitor.show', resource_id=monitor.id), 302)

############
## DELETE ##
############

@bp.route("/<int:resource_id>/delete", methods=("POST",))
@login_required
def delete(resource_id):
  form = MonitorDeleteForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message="Monitor deletion failed",
      reasons=form.errors
    ))

  try:
    delete_resource(Monitor, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message="Monitor deletion failed",
      reasons=dict(monitor=[error.message])
    ))

  return redirect(url_for('monitor.list'), 302)
