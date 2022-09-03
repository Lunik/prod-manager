
from ProdManager import create_app

from ProdManager.models.Maintenance import (
  MaintenanceStatus, Maintenance,
)

app = create_app()

def test_maintenance_title():
  maintenance = Maintenance(
    name="UNIT-TEST",
    status=MaintenanceStatus.SCHEDULED
  )

  assert "UNIT-TEST" in maintenance.title

  maintenance = Maintenance(
    name="UNIT-TEST",
    external_reference="CHG00001",
    status=MaintenanceStatus.SCHEDULED
  )

  assert "UNIT-TEST" in maintenance.title
  assert "CHG00001" in maintenance.title


def test_count_maintenances():
  with app.app_context():
    maintenance_count = Maintenance.count_by_status(Maintenance.query)

    for status in MaintenanceStatus:
      assert type(maintenance_count[status]) == int

  with app.app_context():
    maintenance_count = Maintenance.count_by_status(Maintenance.query, serialize=True)

    for status in MaintenanceStatus:
      assert type(maintenance_count[status.value]) == int