
from flask import Blueprint

from ProdManager.models import (
  Incident, Maintenance, Monitor
)
from ProdManager.helpers.resource import list_resources
from ProdManager.helpers.template import custom_render_template

bp = Blueprint("root", __name__, url_prefix="/")


@bp.route('/')
def index():
  return custom_render_template("index.html",
    ongoing_incidents=list_resources(
      Incident,
      filters=Incident.ongoing_filter(),
      orders=Incident.reverse_order(),
      paginate=False,
      limit=10,
    ),
    past_incidents=list_resources(
      Incident,
      filters=Incident.past_filter(),
      paginate=False,
      limit=10,
    ),
    scheduled_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.scheduled_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
      limit=10,
    ),
    ongoing_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.ongoing_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
      limit=10,
    ),
    past_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.past_filter(),
      paginate=False,
      limit=10,
    ),
    monitors_count=Monitor.count_monitors(Monitor.query),
  ), 200

@bp.route('/about')
def about():
  return custom_render_template("about.html"), 200

@bp.route('/api')
def swagger():
  return custom_render_template("swagger.html"), 200
