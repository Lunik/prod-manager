
from ProdManager import create_app

from ProdManager.models.Incident import (
  IncidentSeverity, IncidentStatus,
  Incident,
)

app = create_app()

def test_incident_title():
  incident = Incident(
    name="UNIT-TEST",
    severity=IncidentSeverity.CRITICAL,
    status=IncidentStatus.ACTIVE
  )

  assert "UNIT-TEST" in incident.title

  incident = Incident(
    name="UNIT-TEST",
    severity=IncidentSeverity.CRITICAL,
    external_reference="CHG00001",
    status=IncidentStatus.ACTIVE
  )

  assert "UNIT-TEST" in incident.title
  assert "CHG00001" in incident.title


def test_count_incidents():
  with app.app_context():
    incident_count = Incident.count_by_status(Incident.query)

    for status in IncidentStatus:
      assert type(incident_count[status]) == int

  with app.app_context():
    incident_count = Incident.count_by_status(Incident.query, serialize=True)

    for status in IncidentStatus:
      assert type(incident_count[status.value]) == int