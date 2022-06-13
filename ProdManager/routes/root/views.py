
from flask import Blueprint, render_template

from ProdManager.models.Incident import Incident
from ProdManager.models.Maintenance import Maintenance
from ProdManager.helpers.resource import list_resources

bp = Blueprint("root", __name__, url_prefix="/")


@bp.route('/')
def index():
  return render_template("index.html",
    ongoing_incidents=list_resources(
      Incident,
      filters=Incident.ongoing_filter(),
      paginate=False,
    ),
    past_incidents=list_resources(
      Incident,
      filters=Incident.past_filter(),
      paginate=False,
    ),
    ongoing_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.ongoing_filter(),
      paginate=False,
    ),
    past_maintenances=list_resources(
      Maintenance,
      filters=Maintenance.past_filter(),
      paginate=False,
    ),
  ), 200

@bp.route('/about')
def about():
  return render_template("about.html"), 200
