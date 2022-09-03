from flask import Blueprint

from ProdManager.helpers.template import custom_render_template

from ProdManager.models import (
  Monitor, Maintenance, Incident
)

bp = Blueprint("weather", __name__)

#############
## WEATHER ##
#############

@bp.route("/monitor", methods=("GET",))
def monitor():
  monitors = Monitor.count_by_status(Monitor.query, serialize=True)

  return custom_render_template(None,
    json=dict(resources=monitors, serialize=False),
  )

@bp.route("/maintenance", methods=("GET",))
def maintenance():
  maintenances = Maintenance.count_by_status(Maintenance.query, serialize=True)

  return custom_render_template(None,
    json=dict(resources=maintenances, serialize=False),
  )

@bp.route("/incident", methods=("GET",))
def incident():
  incidents = Incident.count_by_status(Incident.query, serialize=True)

  return custom_render_template(None,
    json=dict(resources=incidents, serialize=False),
  )
