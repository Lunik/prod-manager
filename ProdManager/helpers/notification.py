import enum

from flask import current_app

from ProdManager.plugins import mail, lang

from ProdManager.models import Subscriber, Incident, Maintenance
from ProdManager.helpers.template import custom_render_template
import ProdManager.helpers.resource as ResourceHelpers


NOTIFICATION_SUPPORTED_RESOURCES = [
  Incident, Maintenance,
]


class NotificationType(enum.Enum):
  CREATE = "create"
  UPDATE = "update"


def send_notification(title, content):
  return mail.send_mail(
    [subscriber.email for subscriber in ResourceHelpers.list_resources(Subscriber, paginate=False)],
    title,
    content,
  )


def notify(notif_type, resource_class, resource):
  if not isinstance(notif_type, NotificationType):
    raise Exception("notif_type is not of type : NotificationType")

  if resource_class not in NOTIFICATION_SUPPORTED_RESOURCES:
    current_app.logger.debug(
      f"Ignore sending notification because {resource_class} is not in {NOTIFICATION_SUPPORTED_RESOURCES}"
    )
    return

  notif_title = resource.title
  notif_title += " - " + lang.get(f"{resource_class.__name__.lower()}_{notif_type.value}_notification_title")

  try:
    send_notification(notif_title, custom_render_template(
      f"notification/{resource_class.__name__.lower()}.html",
      resource=resource,
    ))
  except Exception as error:
    current_app.logger.error(f"Unable to send notification during {resource_class.__name__} {notif_type.value} : {error}")
