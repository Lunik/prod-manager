
from flask import Blueprint, render_template

from ProdManager.models.Incident import Incident, filter_ongoing_incident, filter_past_incident
from ProdManager.models.Maintenance import Maintenance, filter_ongoing_maintenance, filter_past_maintenance

bp = Blueprint("root", __name__, url_prefix="/")


@bp.route('/')
def index():
  incident_query = Incident.query.order_by(Incident.creation_date.desc())
  maintenance_query = Maintenance.query.order_by(Maintenance.creation_date.desc())

  return render_template("index.html",
    ongoing_incidents=filter_ongoing_incident(incident_query),
    past_incidents=filter_past_incident(incident_query),
    ongoing_maintenances=filter_ongoing_maintenance(maintenance_query),
    past_maintenances=filter_past_maintenance(maintenance_query),
  ), 200

@bp.route('/about')
def about():
  return render_template("about.html"), 200
