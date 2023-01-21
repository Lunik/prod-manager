
from flask import Blueprint, current_app

from ProdManager.models import (
  Incident, Maintenance, Monitor
)
from ProdManager.helpers.resource import list_resources
from ProdManager.helpers.template import custom_render_template

bp = Blueprint("root", __name__, url_prefix="/")


@bp.route('/')
def index():
  return custom_render_template("index.html",
    ongoing_incidents_filters=Incident.ongoing_filter(raw=True),
    ongoing_incidents=list_resources(
      Incident,
      filters=Incident.ongoing_filter(),
      orders=Incident.reverse_order(),
      paginate=False,
      limit=10,
    ),
    past_incidents_filters=Incident.past_filter(raw=True),
    scheduled_maintenances_filters=Maintenance.scheduled_filter(raw=True),
    scheduled_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.scheduled_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
      limit=10,
    ),
    ongoing_maintenances_filters=Maintenance.ongoing_filter(raw=True),
    ongoing_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.ongoing_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
      limit=10,
    ),
    past_maintenances_filters=Maintenance.past_filter(raw=True),
    monitors_count=Monitor.count_by_status(),
  ), 200

@bp.route('/about')
def about():
  return custom_render_template("about.html"), 200

@bp.route('/api')
def swagger():
  return custom_render_template("swagger.html"), 200

@bp.route('/robots.txt')
def robots():
  return current_app.send_static_file('robots.txt')
