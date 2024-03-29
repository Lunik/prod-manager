
from ProdManager import create_app

from ProdManager.models.Monitor import (
  MonitorStatus, Monitor,
)

app = create_app(scheduled_jobs=False)

def test_monitor_count_by_status():
  with app.app_context():
    monitor_count = Monitor.count_by_status()

    for status in MonitorStatus:
      assert type(monitor_count[status]) == int

  with app.app_context():
    monitor_count = Monitor.count_by_status(serialize=True)

    for status in MonitorStatus:
      assert type(monitor_count[status.value]) == int

  with app.app_context():
    monitor_count = Monitor.count_by_status(serialize=True, filters=(Monitor.scope_id == 1,))

    for status in MonitorStatus:
      assert type(monitor_count[status.value]) == int
