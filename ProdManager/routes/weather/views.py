from flask import Blueprint

from ProdManager.helpers.template import custom_render_template
from ProdManager.helpers.resource import resource_filters
from ProdManager.models import (
  Monitor, Maintenance, Incident
)

bp = Blueprint("weather", __name__)

#############
## WEATHER ##
#############

@bp.route("/monitor", methods=("GET",))
@resource_filters(Monitor.filters())
def monitor(filters):
  monitors = Monitor.count_by_status(serialize=True, filters=filters)

  return custom_render_template(None,
    json=dict(resources=monitors, serialize=False),
  )

@bp.route("/maintenance", methods=("GET",))
@resource_filters(Maintenance.filters())
def maintenance(filters):
  maintenances = Maintenance.count_by_status(serialize=True, filters=filters)

  return custom_render_template(None,
    json=dict(resources=maintenances, serialize=False),
  )

@bp.route("/incident", methods=("GET",))
@resource_filters(Incident.filters())
def incident(filters):
  incidents = Incident.count_by_status(serialize=True, filters=filters)

  return custom_render_template(None,
    json=dict(resources=incidents, serialize=False),
  )
