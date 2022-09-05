
from ProdManager import create_app

from ProdManager.models.Monitor import (
  MonitorStatus, Monitor,
)

app = create_app()

def test_monitor_count_by_status():
  with app.app_context():
    monitor_count = Monitor.count_by_status(Monitor.query)

    for status in MonitorStatus:
      assert type(monitor_count[status]) == int

  with app.app_context():
    monitor_count = Monitor.count_by_status(Monitor.query, serialize=True)

    for status in MonitorStatus:
      assert type(monitor_count[status.value]) == int

  with app.app_context():
    monitor_count = Monitor.count_by_status(Monitor.query, serialize=True, filters=(Monitor.scope_id == 1,))

    for status in MonitorStatus:
      assert type(monitor_count[status.value]) == int
