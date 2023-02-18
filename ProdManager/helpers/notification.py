import enum

from flask import current_app

from ProdManager.plugins import mail, lang

from ProdManager.models import Subscriber, Incident, Maintenance, Announcement
from ProdManager.helpers.template import custom_render_template
import ProdManager.helpers.resource as ResourceHelpers


NOTIFICATION_SUPPORTED_RESOURCES = [
  Incident, Maintenance, Announcement
]


class NotificationType(enum.Enum):
  CREATE = "create"
  UPDATE = "update"


def send_notification(title, content, attachments=[]):
  return mail.send_mail(
    to_emails=[subscriber.email for subscriber in ResourceHelpers.list_resources(Subscriber, paginate=False)],
    subject=title,
    body=content,
    attachments=attachments,
  )


def notify(notif_type, resource_class, resource):
  if not isinstance(notif_type, NotificationType):
    raise Exception("notif_type is not of type : NotificationType")

  if resource_class not in NOTIFICATION_SUPPORTED_RESOURCES:
    current_app.logger.debug(
      "Ignore sending notification because %s is not in %s",
      resource_class,
      NOTIFICATION_SUPPORTED_RESOURCES,
    )
    return

  notif_title = resource.title
  notif_title += " - " + lang.get(f"{resource_class.__name__.lower()}_{notif_type.value}_notification_title")

  try:
    send_notification(
      title=notif_title,
      content=custom_render_template(
        f"notification/{resource_class.__name__.lower()}.html",
        resource=resource,
        minify=False,
      ),
      attachments=resource.notify_attachments(),
    )
  except Exception as error:
    current_app.logger.error(
      "Unable to send notification during %s %s : %s",
      resource_class.__name__,
      notif_type.value,
      error,
    )
