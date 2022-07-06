
from flask import Blueprint, render_template

from ProdManager.models import (
  Incident, Maintenance, Monitor
)
from ProdManager.helpers.resource import list_resources

bp = Blueprint("root", __name__, url_prefix="/")


@bp.route('/')
def index():
  return render_template("index.html",
    ongoing_incidents=list_resources(
      Incident,
      filters=Incident.ongoing_filter(),
      orders=Incident.reverse_order(),
      paginate=False,
    ),
    past_incidents=list_resources(
      Incident,
      filters=Incident.past_filter(),
      paginate=False,
    ),
    scheduled_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.scheduled_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
    ),
    ongoing_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.ongoing_filter(),
      orders=Maintenance.reverse_order(),
      paginate=False,
    ),
    past_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.past_filter(),
      paginate=False,
    ),
    monitors_count=Monitor.count_monitors(Monitor.query),
  ), 200

@bp.route('/about')
def about():
  return render_template("about.html"), 200
