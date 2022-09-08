from unittest import mock, TestCase
from flask import g

from ProdManager.models import (
  Maintenance, MaintenanceStatus,
  Scope, Service, ServiceStatus
)
from ProdManager.helpers.notification import (
  send_notification, notify, NotificationType
)
from ProdManager import create_app

app = create_app()
app.config["SERVER_NAME"] = "ti.example.org"

@mock.patch('ProdManager.helpers.notification.send_notification')
def test_notify(mock_instance):
  with app.app_context():
    g.api = False
    notify(NotificationType.CREATE, Maintenance, Maintenance(
      id=1,
      scope=Scope(id=1, name="scp01"),
      service=Service(id=1, name="svc01"),
      name="maint01",
      status=MaintenanceStatus.FAILED,
      service_status=ServiceStatus.UP
    ))

    mock_instance.assert_called_once()

@mock.patch('ProdManager.helpers.notification.send_notification')
def test_notify_2(mock_instance):
  with app.app_context():
    g.api = False
    notify(NotificationType.CREATE, Scope, Scope(id=1, name="scp01"))

    mock_instance.assert_not_called()

def test_notify_3():
  with app.app_context():
    g.api = False
    with TestCase().assertRaises(Exception):
      notify(None, Scope, Scope(id=1, name="scp01"))
