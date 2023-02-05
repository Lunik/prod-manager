from flask import Blueprint, redirect, abort

from ProdManager.plugins import lang

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
from ProdManager.helpers.links import custom_url_for

from ProdManager.models import (
  AnnouncementLevel, Announcement, Scope, Service
)

from .forms import (
  AnnouncementCreateForm, AnnouncementUpdateForm, AnnouncementDeleteForm
)

bp = Blueprint("announcement", __name__)

##########
## LIST ##
##########

@bp.route("", methods=("GET",))
@resource_filters(Announcement.filters())
def list(filters):
  announcements = list_resources(Announcement, filters=filters)

  create_form = AnnouncementCreateForm()
  create_form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  create_form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  return custom_render_template("announcement/list.html",
    announcements=announcements,
    json=dict(resources=announcements),
    create_form=create_form,
    filters=Announcement.filters().keys(),
  ), 200


############
## CREATE ##
############

@bp.route("/create", methods=("POST",))
@login_required
def create():
  form=AnnouncementCreateForm()
  form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("announcement_creation_failed"),
      reasons=form.errors
    ))

  try:
    announcement = create_resource(Announcement, dict(
      name=strip_input(form.name.data),
      description=strip_input(form.description.data),
      scope_id=int(form.scope.data),
      service_id=int(form.service.data),
      creation_date=current_date(),
      start_date=form.start_date.data,
      end_date=form.end_date.data,
      level=AnnouncementLevel(form.level.data),
    ))
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("announcement_creation_failed"),
      reasons=dict(announcement=[error.message])
    ))

  return redirect(custom_url_for('announcement.show', resource_id=announcement.id), 302)

##########
## SHOW ##
##########

@bp.route("/<int:resource_id>", methods=("GET",))
def show(resource_id):
  try:
    announcement = get_resource(Announcement, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("announcement_show_failed"),
      reasons=dict(announcement=[error.message])
    ))

  update_form = AnnouncementUpdateForm(obj=announcement)
  update_form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  update_form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  update_form.scope.default = announcement.scope.id
  update_form.service.default = announcement.service.id
  update_form.scope.process(formdata=None)
  update_form.service.process(formdata=None)

  return custom_render_template("announcement/single.html",
    announcement=announcement,
    json=dict(resources=announcement),
    update_form=update_form,
    delete_form=AnnouncementDeleteForm(obj=announcement)
  ), 200


############
## UPDATE ##
############

@bp.route("/<int:resource_id>/update", methods=("POST",))
@login_required
def update(resource_id):
  form = AnnouncementUpdateForm()
  form.scope.choices = list_resources_as_choices(Scope, Scope.name.asc())
  form.service.choices = list_resources_as_choices(Service, Service.name.asc())

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get("announcement_update_failed"),
      reasons=form.errors
    ))

  new_announcement_level = AnnouncementLevel(form.level.data)
  new_data = dict(
    name=strip_input(form.name.data),
    description=strip_input(form.description.data),
    level=new_announcement_level,
    start_date=form.start_date.data,
    end_date=form.end_date.data,
    scope_id=int(form.scope.data),
    service_id=int(form.service.data),
  )

  try:
    announcement, _ = update_resource(Announcement, resource_id, new_data)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get("announcement_update_failed"),
      reasons=dict(announcement=[error.message])
    ))

  return redirect(custom_url_for('announcement.show', resource_id=announcement.id), 302)

############
## DELETE ##
############

@bp.route("/<int:resource_id>/delete", methods=("POST",))
@login_required
def delete(resource_id):
  form = AnnouncementDeleteForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message=lang.get('announcement_deletion_failed'),
      reasons=form.errors
    ))

  try:
    delete_resource(Announcement, resource_id)
  except Exception as error:
    return abort(error.code, dict(
      message=lang.get('announcement_deletion_failed'),
      reasons=dict(announcement=[error.message])
    ))

  return redirect(custom_url_for('announcement.list'), 302)
