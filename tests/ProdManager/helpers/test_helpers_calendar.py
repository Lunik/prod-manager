from datetime import datetime

from ProdManager.helpers.calendar import CalendarEvent
from ProdManager.helpers.date import current_date
from ProdManager.models import (
  Maintenance, MaintenanceStatus,
  Scope,
  Service, ServiceStatus,
)
from ProdManager import create_app

app = create_app()
app.config['SERVER_NAME'] = "pytest"

def test_calendar():
  with app.app_context():
    maintenance = Maintenance(
      id = 1,
      name = "TEST maintenance",
      description = "The wonderfull description\nsecond line",
      external_reference = "CHG0000000",
      status = MaintenanceStatus.SCHEDULED,
      service_status = ServiceStatus.DOWN,
      creation_date = current_date(),
      scheduled_start_date = datetime(year=2022, month=1, day=1, hour=18, minute=00),
      scheduled_end_date = datetime(year=2022, month=1, day=1, hour=20, minute=00),
    )

    maintenance.scope = Scope(name="test")
    maintenance.service = Service(name="test")


    calendar = CalendarEvent.from_maintenance(maintenance)

    ics_data = calendar.render()

    assert "BEGIN:VCALENDAR" in str(ics_data)
    assert "SUMMARY:[CHG0000000] TEST maintenance" in str(ics_data)

def test_calendar():
  with app.app_context():
    maintenance = Maintenance(
      id = 1,
      name = "TEST maintenance",
      description = "The wonderfull description\nsecond line",
      status = MaintenanceStatus.SCHEDULED,
      service_status = ServiceStatus.DOWN,
      creation_date = current_date(),
      scheduled_start_date = datetime(year=2022, month=1, day=1, hour=18, minute=00),
      scheduled_end_date = datetime(year=2022, month=1, day=1, hour=20, minute=00),
    )

    maintenance.scope = Scope(name="test")
    maintenance.service = Service(name="test")


    calendar = CalendarEvent.from_maintenance(maintenance)

    ics_data = calendar.render()

    assert "BEGIN:VCALENDAR" in str(ics_data)
    assert "SUMMARY:TEST maintenance" in str(ics_data)